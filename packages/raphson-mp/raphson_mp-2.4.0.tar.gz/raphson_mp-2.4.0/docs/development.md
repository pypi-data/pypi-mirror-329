# Development

## Development using Docker

With `docker` and `docker-compose-plugin` installed, run the following command to start a local testing server:
```
docker compose up --build
```

Before doing so, you will need to create a music and data directory. You may need to change `user` in the `compose.yaml` file if your user is not using the default id of 1000.

## Development without Docker

Install as an [editable installation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html):
```
pip install --editable .
```

Start the web server in development mode, which supports live reloading:
```
raphson-mp start --dev
```

If `~/.local/bin` is not on your path and you don't want to add it, you can use `python3 -m raphson_mp` instead.

pyproject.toml specifies the project's dependencies, which you [have to install manually](https://github.com/pypa/pip/issues/11440) using pip for now.

To reduce the numer of packages that need to be installed by Pip, you can install system packages before running pip install (this list may be outdated):
```
sudo dnf install python3-aiohttp python3-babel python3-jinja2 yt-dlp babel poedit python3-build twine python3-pytest python3-pytest-asyncio
```

## Code structure

  * (`data/`): default database directory.
  * `docker/`: additional files used to build containers.
  * `docs/`: documentation in markdown format.
  * (`music/`): default music directory.
  * `raphson_mp/`: contains program source code
    * `client/`: helpers for client applications
    * `common/`: shared data structures for both the server and clients
    * `migrations/`: sql files used to update the database.
    * `routes`: files containing route functions (marked with `@route`)
    * `sql/`: sql files used to initialize the database, also useful as a database layout reference.
    * `static/`: static files that are served as-is by the frontend, under the `/static` URL. The files in `/static/js/player/*.js` are served in concatenated form as `/static/js/player.js`.
    * `templates/`: jinja2 template files for web pages.
    * `translations/`: translation files, see translations section.

## Code style

Use `make format` to ensure proper code style. `pyproject.toml` contains some settings which should be picked up automatically.

## Preparing for development while offline

### Docker images

If you wish to use Docker for development, use `docker pull` to download the base image (first line of Dockerfile). If you don't do this, buildx will attempt to pull the image very frequently while rebuilding, which won't work offline.

Then, build and start the container: `docker compose up --build`. Following builds will be cached, unless you change one of the `RUN` instructions in the `Dockerfile`.

### Music

Add some music to `./music`. Adding only a small amount is recommended. While online, start the web interface, enable all playlists and skip through all tracks. This will ensure album art and lyrics are downloaded to the cache for all tracks.

## Translations

### For developers

In templates:
```jinja
{% trans %}Something in English{% endtrans %}
{{ gettext('Something in English') }}
```

In Python:
```py
from i18n import gettext

translated_string = gettext('Something in English')
```

### For translators

1. Run `make update-messages`
2. Edit the `messages.po` file in `raphson_mp/translations/<language_code>/LC_MESSAGES/` using a text editor or PO editor like Poedit. To create a new language, run: `pybabel init -i messages.pot -d raphson_mp/translations -l <language_code>`
3. Run `make update-messages` again to ensure the language files are in a consistent format, regardless of your PO editor.
4. To actually see your changes, run `make compile-messages` and restart the server.

## Testing

Run all tests, except for online tests: `make test`

Run all tests: `make testall`

⚠️ Do not run all tests too often. Web scraping can trigger rate limits, especially in the case of automated tests which make the same requests every time.

Run a specific test: `pytest tests/test_server.py`

Measure code coverage:
```
make testall
make coverage
```

Test coverage history:

| Date       | Total code coverage
| ---------- | -------------------
| 2024-12-05 | 48%
| 2024-12-09 | 54%
| 2024-12-11 | 56%
| 2024-12-13 | 60%
| 2024-12-21 | 61%
| 2024-12-24 | 63%
| 2024-01-18 | 62%
| 2024-02-18 | 66%
| 2024-02-21 | 71%

## Release

* Run tests: `make testall`
* Update version in `pyproject.toml`
* Update changelog in `CHANGES.md`
* Deploy to pypi: `make deploy-pypi`
* Deploy to docker hub: `make deploy-docker`
* Update Debian changelog (`debian/changelog`). Get the date using `date -R`
* Build new Debian package and upload it to the repo (manually for now)
* Commit and create a tag
