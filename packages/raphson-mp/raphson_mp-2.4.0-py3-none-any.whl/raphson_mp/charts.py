import asyncio
import logging
import time
from collections.abc import Callable
from enum import Enum, unique
from sqlite3 import Connection
from typing import Any, cast

from raphson_mp import cache
from raphson_mp.i18n import gettext as _

ChartT = dict[str, Any]
LegendT = list[str]
DataT = dict[str, list[int]]
SeriesT = list[dict[str, str | list[int]]]
HeatmapDataT = list[tuple[int, int, float]]
HeatmapSeriesT = list[dict[str, str | HeatmapDataT]]

_LOGGER = logging.getLogger(__name__)


@unique
class StatsPeriod(Enum):
    DAY = 24 * 60 * 60
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY
    ALL = 0

    @property
    def after_timestamp(self):
        if self is StatsPeriod.ALL:
            return 0
        else:
            return int(time.time()) - self.value

    @staticmethod
    def from_str(period: str) -> "StatsPeriod":
        if period == "day":
            return StatsPeriod.DAY
        elif period == "week":
            return StatsPeriod.WEEK
        elif period == "month":
            return StatsPeriod.MONTH
        elif period == "year":
            return StatsPeriod.YEAR
        elif period == "all":
            return StatsPeriod.ALL

        raise ValueError()


def chart(
    title: str,
    ldata: LegendT,
    xdata: list[str] | list[int] | None,
    ydata: list[str] | list[int] | None,
    series: SeriesT | HeatmapSeriesT,
    xname: str,
    yname: str,
    all_labels: bool = False,
    extra: dict[str, Any] | None = None,
) -> ChartT:
    assert xdata is not None or ydata is not None
    if extra is None:
        extra = {}
    chart: dict[str, Any] = {
        "title": {"text": title},
        "tooltip": {},
        "legend": {
            "orient": "vertical",
            "right": 0,
            "top": "center",
            "type": "scroll",
            "data": ldata,
        },
        "xAxis": {
            "type": "category" if xdata else "value",
            "data": xdata,
            "name": xname,
        },
        "yAxis": {
            "type": "category" if ydata else "value",
            "data": ydata,
            "name": yname,
        },
        "series": series,
        **extra,
    }

    if ydata and not xdata:
        chart["yAxis"]["inverse"] = True

    if all_labels:
        for axis in ("xAxis", "yAxis"):
            chart[axis]["axisLabel"] = {"interval": 0}

    return chart


def bar(
    title: str,
    axisdata: list[str] | list[int],
    seriesdata: DataT,
    xname: str,
    yname: str,
    horizontal: bool = False,
    all_labels: bool = False,
) -> ChartT:
    series = [{"name": name, "type": "bar", "stack": "x", "data": data} for name, data in seriesdata.items()]
    ldata = [name for name, _ in seriesdata.items()]
    xdata = axisdata if not horizontal else None
    ydata = axisdata if horizontal else None
    return chart(title, ldata, xdata, ydata, series, xname, yname, all_labels=all_labels)


def heatmap(
    title: str,
    name: str,
    xdata: LegendT,
    ydata: LegendT,
    seriesdata: HeatmapDataT,
    xname: str,
    yname: str,
) -> ChartT:
    series = [{"name": name, "type": "heatmap", "data": seriesdata}]
    extra = {
        "visualMap": {
            "min": 0,
            "max": max(item[2] for item in seriesdata) if len(seriesdata) else 0,
            "orient": "vertical",
            "right": 0,
            "top": "center",
        }
    }
    return chart(title, [], xdata, ydata, series, xname, yname, all_labels=True, extra=extra)


def rows_to_xy(name: str, rows: list[tuple[str, int]]) -> tuple[list[str], DataT]:
    """
    Convert rows as returned by sqlite .fetchall() for query:
        SELECT column, COUNT(*) GROUP BY column
    Returns: axisdata, seriesdata for bar() function
    """
    return [row[0] for row in rows], {name: [row[1] for row in rows]}


def rows_to_xy_multi(
    rows: list[tuple[str, str, int]],
    case_sensitive: bool = True,
    restore_case: bool = False,
    a_limit: int | None = None,
) -> tuple[list[str], DataT]:
    """
    Convert rows as returned by sqlite .fetchall() for query:
        SELECT column_a, column_b, COUNT(*) GROUP BY column_a, column_b
    Input:
    [a1, b1, c1]
    [a1, b2, c2]
    [a2, b1, c3]
    Returns:
    Tuple of axisdata: [a1, a2] and seriesdata: {b1: [c1, c3], b2: [c2, 0]
    Where a appears on the x axis, b appears in the legend (is stacked), and c is data.
    For bar() function.
    """
    if restore_case:
        assert not case_sensitive, "restore_case makes no sense if case sensitive"

    # Create list of a values, sorted by total b for every a
    a_list: list[str] = []
    a_counts: dict[str, int] = {}  # for sorting
    for a, _b, c in rows:
        if not case_sensitive:
            a = a.lower()

        if a not in a_list:
            a_list.append(a)
            a_counts[a] = 0

        a_counts[a if case_sensitive else a.lower()] += c

    axisdata = sorted(a_list, key=lambda a: -a_counts[a])

    if a_limit is not None and len(axisdata) > a_limit:
        axisdata = axisdata[:a_limit]

    seriesdata: DataT = {}

    for a, b, c in rows:
        try:
            a_index = axisdata.index(a if case_sensitive else a.lower())
        except ValueError:
            continue  # outside of limit
        if b not in seriesdata:
            seriesdata[b] = [0] * len(axisdata)
        seriesdata[b][a_index] = c

    if restore_case:
        # Restore original case
        for i, a in enumerate(axisdata):
            for a2, _b, _c in rows:
                if a.lower() == a2.lower():
                    axisdata[i] = a2
                    break

    return axisdata, seriesdata


def chart_last_chosen(conn: Connection) -> ChartT:
    """
    Last chosen chart
    """
    cur = conn.cursor()
    result_playlists = [row[0] for row in cur.execute("SELECT playlist FROM track GROUP BY playlist ORDER BY playlist")]
    result_week = cur.execute(
        "SELECT playlist, COUNT(last_chosen) FROM track WHERE unixepoch() - last_chosen <= 60*60*24*7 GROUP BY playlist ORDER BY playlist"
    ).fetchall()
    result_month = cur.execute(
        "SELECT playlist, COUNT(last_chosen) FROM track WHERE unixepoch() - last_chosen <= 60*60*24*30 AND unixepoch() - last_chosen > 60*60*24*7 GROUP BY playlist ORDER BY playlist"
    ).fetchall()
    result_year = cur.execute(
        "SELECT playlist, COUNT(last_chosen) FROM track WHERE unixepoch() - last_chosen <= 60*60*24*365 AND unixepoch() - last_chosen > 60*60*24*30 GROUP BY playlist ORDER BY playlist"
    ).fetchall()
    result_long_ago = cur.execute(
        "SELECT playlist, COUNT(last_chosen) FROM track WHERE unixepoch() - last_chosen > 60*60*24*365 AND last_chosen != 0 GROUP BY playlist ORDER BY playlist"
    ).fetchall()
    result_never = cur.execute(
        "SELECT playlist, COUNT(last_chosen) FROM track WHERE last_chosen == 0 GROUP BY playlist ORDER BY playlist"
    ).fetchall()

    axis = [_("Last week"), _("Last month"), _("Last year"), _("Long ago"), _("Never")]
    series: DataT = {}

    for playlist in result_playlists:
        series[playlist] = [0] * 6

    for i, result in enumerate((result_week, result_month, result_year, result_long_ago, result_never)):
        for playlist, count in result:
            series[playlist][i] = count

    return bar(_("When tracks were last chosen by algorithm"), axis, series, _("time ago"), _("track count"))


def chart_playlist_track_count(conn: Connection) -> ChartT:
    counts = conn.execute("SELECT playlist, COUNT(*) FROM track GROUP BY playlist ORDER BY COUNT(*) DESC").fetchall()
    return bar(_("Number of tracks in playlists"), *rows_to_xy(_("Number of tracks"), counts), _("playlist"), _("track count"))


def chart_playlist_track_mean_duration(conn: Connection) -> ChartT:
    means = conn.execute(
        "SELECT playlist, AVG(duration)/60 FROM track GROUP BY playlist ORDER BY AVG(duration) DESC"
    ).fetchall()
    return bar(_("Mean duration of tracks in playlists"), *rows_to_xy(_("Track duration"), means), _("playlist"), _("duration (seconds)"))


def chart_playlist_total_duration(conn: Connection) -> ChartT:
    totals = conn.execute(
        "SELECT playlist, SUM(duration)/60 FROM track GROUP BY playlist ORDER BY SUM(duration) DESC"
    ).fetchall()
    return bar(_("Total duration of tracks in playlists"), *rows_to_xy(_("Track duration"), totals), _("playlist"), _("duration (seconds)"))


def chart_track_year(conn: Connection) -> ChartT:
    """
    Track release year chart
    """
    min_year, max_year = conn.execute("SELECT MAX(1950, MIN(year)), MIN(2030, MAX(year)) FROM track").fetchone()

    data: dict[str, list[int]] = {}

    if min_year and max_year:
        for (playlist,) in conn.execute(
            "SELECT playlist FROM track GROUP BY playlist ORDER BY COUNT(*) DESC LIMIT 15"
        ).fetchall():
            data[playlist] = [0] * (max_year - min_year + 1)

        rows = conn.execute(
            """
            SELECT playlist, year, COUNT(year)
            FROM track
            WHERE year IS NOT NULL
            GROUP BY playlist, year
            ORDER BY year ASC
            """
        ).fetchall()
        for playlist, year, count in rows:
            if year < min_year or year > max_year or playlist not in data:
                continue
            data[playlist][year - min_year] = count

    return bar(_("Track release year distribution"), [str(year) for year in range(min_year, max_year + 1)], data, _("year"), _("track count"))


def chart_users(conn: Connection, period: StatsPeriod) -> ChartT:
    rows = conn.execute(
        """
        SELECT username, playlist, COUNT(*)
        FROM history JOIN user ON history.user = user.id
        WHERE timestamp > ?
        GROUP BY user, playlist
        """,
        (period.after_timestamp,),
    ).fetchall()
    return bar(_("Active users"), *rows_to_xy_multi(rows, a_limit=15), _("user"), _("play count"), all_labels=True)


def chart_playlists(conn: Connection, period: StatsPeriod) -> ChartT:
    # the same as chart_users but with two columns swapped
    rows = conn.execute(
        """
        SELECT playlist, username, COUNT(*)
        FROM history JOIN user ON history.user = user.id
        WHERE timestamp > ?
        GROUP BY user, playlist
        """,
        (period.after_timestamp,),
    ).fetchall()
    return bar(_("Played playlists"), *rows_to_xy_multi(rows, a_limit=15), _("playlist"), _("play count"), all_labels=True)


def chart_tracks(conn: Connection, period: StatsPeriod) -> ChartT:
    rows = conn.execute(
        """
        SELECT track, username, COUNT(*)
        FROM history
            JOIN user ON history.user = user.id
        WHERE timestamp > ?
            AND track IN (SELECT track
                            FROM history
                            WHERE timestamp > ?
                            GROUP BY track
                            ORDER BY COUNT(*) DESC
                            LIMIT 10)
        GROUP BY track, username
        """,
        (
            period.after_timestamp,
            period.after_timestamp,
        ),
    ).fetchall()
    return bar(_("Most played tracks"), *rows_to_xy_multi(rows), _("play count"), _("track"), horizontal=True)


def chart_artists(conn: Connection, period: StatsPeriod) -> ChartT:
    rows = conn.execute(
        """
        SELECT artist, username, COUNT(*)
        FROM history
            INNER JOIN track ON history.track = track.path
            JOIN track_artist ON track_artist.track = track.path
            JOIN user ON history.user = user.id
        WHERE timestamp > ?
            AND artist IN (SELECT artist
                            FROM history
                                INNER JOIN track ON history.track = track.path
                                JOIN track_artist ON track_artist.track = track.path
                            WHERE timestamp > ?
                            GROUP BY artist
                            ORDER BY COUNT(*) DESC
                            LIMIT 10)
        GROUP BY artist, username
        """,
        (
            period.after_timestamp,
            period.after_timestamp,
        ),
    ).fetchall()
    return bar(
        _("Most played artists"), *rows_to_xy_multi(rows, case_sensitive=False, restore_case=True), _("play count"), _("artist"), horizontal=True
    )


def chart_albums(conn: Connection, period: StatsPeriod) -> ChartT:
    rows = conn.execute(
        """
        SELECT album, username, COUNT(*)
        FROM history
            INNER JOIN track ON history.track = track.path
            JOIN user ON history.user = user.id
        WHERE timestamp > ?
            AND album IN (SELECT album
                            FROM history
                                INNER JOIN track ON history.track = track.path
                            WHERE timestamp > ?
                            GROUP BY album
                            ORDER BY COUNT(*) DESC
                            LIMIT 10)
        GROUP BY album, username
        """,
        (
            period.after_timestamp,
            period.after_timestamp,
        ),
    ).fetchall()
    return bar(
        _("Most played albums"), *rows_to_xy_multi(rows, case_sensitive=False, restore_case=True), _("play count"), _("album"), horizontal=True
    )


def chart_time_of_day(conn: Connection, period: StatsPeriod) -> ChartT:
    time_of_day: DataT = {}

    for hour, username, count in conn.execute(
        """
        SELECT strftime('%H', timestamp, 'unixepoch') AS hour, username, COUNT(*)
        FROM history JOIN user ON history.user = user.id
        WHERE timestamp > ?
        GROUP BY hour, username
        """,
        (period.after_timestamp,),
    ):
        if username not in time_of_day:
            time_of_day[username] = [0] * 24
        time_of_day[username][int(hour)] += count

    return bar(_("Time of day"), [f"{i:02}:00" for i in range(0, 24)], time_of_day, _("hour of day (UTC)"), _("play count"))


def chart_day_of_week(conn: Connection, period: StatsPeriod) -> ChartT:
    series: DataT = {}

    for day, username, count in conn.execute(
        """
        SELECT strftime('%w', timestamp, 'unixepoch') AS day, username, COUNT(*)
        FROM history JOIN user ON history.user = user.id
        WHERE timestamp > ?
        GROUP BY day, username
        """,
        (period.after_timestamp,),
    ):
        if username not in series:
            series[username] = [0] * 7
        series[username][int(day)] += count

    return bar(
        _("Day of week"),
        [_("Sunday"), _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday")],
        series,
        _("day of week"),
        _("play count"),
    )


def chart_week_of_year(conn: Connection, period: StatsPeriod) -> ChartT:
    series: DataT = {}

    for week, username, count in conn.execute(
        """
        SELECT strftime('%W', timestamp, 'unixepoch') AS week, username, COUNT(*)
        FROM history JOIN user ON history.user = user.id
        WHERE timestamp > ?
        GROUP BY week, username
        """,
        (period.after_timestamp,),
    ):
        if username not in series:
            series[username] = [0] * 54
        series[username][int(week)] += count

    return bar(
        _("Plays by week"),
        [str(i) for i in range(1, 55)],
        series,
        _("week number"),
        _("play count")
    )


def chart_unique_artists(conn: Connection) -> ChartT:
    rows = conn.execute(
        """
        SELECT playlist, ROUND(COUNT(DISTINCT artist) / CAST(COUNT(artist) AS float), 2) AS ratio
        FROM track INNER JOIN track_artist ON track.path = track_artist.track
        GROUP BY playlist
        ORDER BY ratio
        """
    ).fetchall()
    return bar(_("Artist diversity"), *rows_to_xy(_("Ratio"), rows), _("playlist"), _("distinct artist ratio"))


def chart_popular_artists(conn: Connection) -> ChartT:
    # TODO try COUNT(*)
    rows = conn.execute(
        f"""
        SELECT artist, playlist, COUNT(artist)
        FROM track INNER JOIN track_artist ON track.path = track_artist.track
        WHERE artist IN (SELECT artist FROM track_artist GROUP BY artist ORDER BY COUNT(artist) DESC LIMIT 15)
        GROUP BY artist, playlist
        """
    ).fetchall()
    return bar(
        _("Artists in playlists"), *rows_to_xy_multi(rows, case_sensitive=False, restore_case=True), _("count"), "artist", horizontal=True,
    )


def chart_popular_tags(conn: Connection) -> ChartT:
    # TODO is case_sensitive=False still needed with COLLATE NOCASE?
    rows = conn.execute(
        f"""
        SELECT tag, playlist, COUNT(tag)
        FROM track INNER JOIN track_tag ON track.path = track_tag.track
        WHERE tag IN (SELECT tag FROM track_tag GROUP BY tag ORDER BY COUNT(tag) DESC LIMIT 15)
        GROUP BY tag, playlist
        """
    ).fetchall()
    return bar(
        _("Tags in playlists"), *rows_to_xy_multi(rows, case_sensitive=False, restore_case=False), _("count"), _("tag"), horizontal=True,
    )


def _chart_artist_similarity(conn: Connection) -> tuple[list[str], list[tuple[int, int, float]]]:
    result = conn.execute(
        """
        SELECT t1.playlist, t2.playlist, COUNT(DISTINCT ta1.artist)
        FROM track_artist ta1
            JOIN track t1 ON ta1.track = t1.path
            JOIN track_artist ta2 ON ta1.artist = ta2.artist
            JOIN track t2 ON ta2.track = t2.path
        GROUP BY t1.playlist, t2.playlist
        """
    )

    matching_artist_counts: dict[tuple[str, str], int] = {}
    for playlist1, playlist2, count in result:
        matching_artist_counts[(playlist1, playlist2)] = count

    rows = conn.execute(
        """
        SELECT track.playlist, COUNT(DISTINCT artist)
        FROM track_artist JOIN track ON track_artist.track = track.path
        GROUP BY track.playlist
        ORDER BY COUNT(DISTINCT track) DESC
        LIMIT 15
        """
    ).fetchall()
    playlists: list[str] = [row[0] for row in rows]
    artist_counts: list[int] = [row[1] for row in rows]

    series: list[tuple[int, int, float]] = []
    for i1, p1 in enumerate(playlists):
        for i2, p2 in enumerate(playlists):
            if i1 == i2:
                continue
            elif (p1, p2) in matching_artist_counts:
                percentage = (matching_artist_counts[(p1, p2)] / (artist_counts[i1] + artist_counts[i2])) * 100
                series.append((i1, i2, round(percentage, 2)))
            else:
                series.append((i1, i2, 0))

    return playlists, series


def chart_artist_similarity(conn: Connection) -> ChartT:
    # Chart is quite slow and I'm not sure how to speed it up. Cache it to improve loading speed when switching
    # between periods.
    data = cast(tuple[list[str], list[tuple[int, int, float]]] | None, cache.memory_get("artist similarity"))
    if data is None:
        data = _chart_artist_similarity(conn)
        cache.memory_store("artist similarity", data, cache.HOUR)
    playlists, series = data
    return heatmap(
        _("Artist similarity"),
        _("Percentage of artists in common"),
        playlists,
        playlists,
        series,
        _("playlist"),
        _("playlist"),
    )


PERIOD_CHARTS: list[Callable[[Connection, StatsPeriod], ChartT]] = [
    chart_users,
    chart_playlists,
    chart_time_of_day,
    chart_day_of_week,
    chart_week_of_year,
    chart_tracks,
    chart_albums,
    chart_artists,
]

CHARTS: list[Callable[[Connection], ChartT]] = [
    chart_artist_similarity,
    chart_popular_artists,
    chart_popular_tags,
    chart_track_year,
    chart_last_chosen,
    chart_playlist_track_count,
    chart_playlist_total_duration,
    chart_playlist_track_mean_duration,
    chart_unique_artists,
]


async def get_data(conn: Connection, period: StatsPeriod) -> list[ChartT]:
    """
    Generate charts as json data for stats.jinja2
    """
    charts: list[ChartT] = []

    for chart in PERIOD_CHARTS:
        start = time.time_ns()
        charts.append(chart(conn, period))
        _LOGGER.debug("generated %s in %sms", chart.__name__, (time.time_ns() - start) / 1000000)
        await asyncio.sleep(0)

    for chart in CHARTS:
        start = time.time_ns()
        charts.append(chart(conn))
        _LOGGER.debug("generated %s in %sms", chart.__name__, (time.time_ns() - start) / 1000000)
        await asyncio.sleep(0)

    return charts
