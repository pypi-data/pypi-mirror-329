"use strict";

// Replace timestamp by formatted time string
document.addEventListener('DOMContentLoaded', () => {
    for (const elem of document.getElementsByClassName('format-timestamp')) {
        elem.dataset.sort = elem.textContent;
        elem.textContent = timestampToString(elem.textContent);
    }

    for (const elem of document.getElementsByClassName('format-duration')) {
        elem.dataset.sort = elem.textContent;
        elem.textContent = durationToString(elem.textContent);
    }
});

/**
 * @param {seconds} seconds
 * @returns {string} formatted duration
 */
function durationToString(seconds) {
    // If you modify this function, also copy it to util.js!
    const isoString = new Date(1000 * seconds).toISOString();
    const days = Math.floor(seconds / (24*60*60));
    const hours = parseInt(isoString.substring(11, 13)) + (days * 24);
    const mmss = isoString.substring(14, 19);
    if (hours == 0) {
        return mmss;
    } else {
        return hours + ':' + mmss;
    }
}

function timestampToString(seconds) {
    if (seconds == 0) {
        return '-';
    } else {
        return new Date(1000 * seconds).toLocaleString();
    }
}

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function choice(arr) {
    return arr[randInt(0, arr.length)];
}

function formatLargeNumber(number) {
    if (number > 1_000_000) {
        return (number / 1_000_000).toFixed(1) + 'M';
    } else if (number > 1_000) {
        return (number / 1_000).toFixed(1) + 'k';
    } else {
        return number + '';
    }
}

/**
 * Create button element containing an icon
 * @param {string} iconName
 * @returns {HTMLButtonElement}
 */
function createIconButton(iconName) {
    const button = document.createElement('button');
    button.classList.add('icon-button');
    const icon = document.createElement('div');
    icon.classList.add('icon', 'icon-' + iconName);
    button.appendChild(icon);
    return button;
}

/**
 * Replace icon in icon button
 * @param {HTMLButtonElement} iconButton
 * @param {string} iconName
 */
function replaceIconButton(iconButton, iconName) {
    /** @type {HTMLElement} */
    const icon = iconButton.firstChild;
    icon.classList.remove(...icon.classList.values());
    icon.classList.add('icon', 'icon-' + iconName);
}

// https://stackoverflow.com/a/2117523
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

/**
 * Throw error if response status code is an error code
 * @param {Response} response
 */
function checkResponseCode(response) {
    if (!response.ok) {
        throw Error('response code ' + response.status);
    }
}

/**
 * @param {string} url
 * @param {object} postDataObject
 * @returns {Promise<Response>}
 */
async function jsonPost(url, postDataObject, checkError = true) {
    postDataObject.csrf = CSRF_TOKEN;
    const options = {
        method: 'POST',
        body: JSON.stringify(postDataObject),
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    };
    const response = await fetch(new Request(url, options));
    if (checkError) {
        checkResponseCode(response);
    }
    return response;
}

async function jsonGet(url, checkError = true) {
    const options = {
        headers: new Headers({
            'Accept': 'application/json'
        }),
    };
    const response = await fetch(new Request(url, options));
    if (checkError) {
        checkResponseCode(response);
    }
    return await response.json();
}

function errorObjectToJson(error) {
    if (error instanceof ErrorEvent) {
        return {
            type: 'ErrorEvent',
            message: error.message,
            file: error.filename,
            line: error.lineno,
            error: errorObjectToJson(error.error),
        }
    }

    if (error instanceof PromiseRejectionEvent) {
        return {
            type: 'PromiseRejectionEvent',
            reason: errorObjectToJson(error.reason),
        }
    }

    if (['string', 'number', 'boolean'].indexOf(typeof(error)) != -1) {
        return {
            type: 'literal',
            value: error,
        }
    }

    if (error instanceof Error) {
        return {
            type: 'Error',
            name: error.name,
            message: error.message,
            stack: error.stack,
        }
    }

    if (error == null) {
        return null;
    }

    return {
        name: 'unknown error object',
        type: typeof(error),
        string: String(error),
    }
}

async function sendErrorReport(error) {
    try {
        const errorJson = JSON.stringify(errorObjectToJson(error));
        await fetch('/report_error', {method: 'POST', body: errorJson, headers: {'Content-Type': 'application/json'}});
    } catch (error2) {
        // need to catch errors, this function must never throw an error or a loop is created
        console.error('unable to report error:', error2)
    }
}

window.addEventListener("error", sendErrorReport);
window.addEventListener("unhandledrejection", sendErrorReport);

// Table sorting
document.addEventListener("DOMContentLoaded", () => {
    /**
     * @param {HTMLTableSectionElement} tbody
     * @param {number} columnIndex
     */
    function sort(tbody, columnIndex) {
        // if the same column is clicked for a second time, sort in reverse
        const mod = tbody.currentSort == columnIndex ? -1 : 1;
        tbody.currentSort = mod == -1 ? undefined : columnIndex;
        console.info("sorting table by column", columnIndex, "order", mod);

        [...tbody.children]
            .sort((row1, row2) => {
                const a = row1.children[columnIndex];
                const b = row2.children[columnIndex];
                const aVal = 'sort' in a.dataset ? parseInt(a.dataset.sort) : a.textContent;
                const bVal = 'sort' in b.dataset ? parseInt(b.dataset.sort) : b.textContent;
                return mod * (aVal > bVal ? 1 : -1);
            })
            .forEach(row => tbody.appendChild(row));
        // interesting behaviour of appendChild: if the node already exists, it is moved from its original location
    }

    for (const tempTable of document.querySelectorAll(".table")) {
        const table = tempTable;
        const thead = table.children[0];
        const tbody = table.children[1];

        if (thead.tagName != "THEAD" || tbody.tagName != "TBODY") {
            console.warn("ignoring invalid table", table);
            continue;
        }

        const tr = thead.children[0];
        for (let i = 0; i < tr.children.length; i++) {
            const columnIndex = i;
            tr.children[i].addEventListener("click", () => {
                sort(tbody, columnIndex)
            });
            tr.children[i].style.cursor = 'pointer';
        }
    }
});
