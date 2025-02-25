function tdIconButton(button) {
    const td = document.createElement("td");
    td.classList.add('button-col');
    td.append(button);
    return td;
}

document.addEventListener('DOMContentLoaded', () => {
    const uploadFilesButton = document.getElementById('upload-files-button');
    const createDirectoryButton = document.getElementById('create-directory-button');

    if (uploadFilesButton) {
        uploadFilesButton.addEventListener('click', () => {
            uploadFilesButton.setAttribute("disabled", "");
            createDirectoryButton.removeAttribute("disabled");
            document.getElementById('create-directory-form').hidden = true;
            document.getElementById('upload-files-form').hidden = false;
        });

        createDirectoryButton.addEventListener('click', () => {
            createDirectoryButton.setAttribute("disabled", "");
            uploadFilesButton.removeAttribute("disabled");
            document.getElementById('create-directory-form').hidden = false;
            document.getElementById('upload-files-form').hidden = true;
        });
    }

    for (const tr of document.getElementById("tbody").children) {
        const path = tr.dataset.path;
        const name = path.split("/").slice(-1)[0];

        // download button
        const downloadButton = createIconButton('download');
        downloadButton.addEventListener('click', () => {
            window.open('/files/download?path=' + encodeURIComponent(path));
        });
        tr.append(tdIconButton(downloadButton));

        // rename button
        if (uploadFilesButton) { // presence of upload button means user has write permissions
            const renameButton = createIconButton('rename-box');
            renameButton.addEventListener('click', () => {
                window.location = '/files/rename?path=' + encodeURIComponent(path);
            });
            tr.append(tdIconButton(renameButton));

            // trash button
            const isTrash = window.location.href.endsWith("&trash"); // TODO properly examine query string
            const trashButton = createIconButton(isTrash ? 'delete-restore' : 'delete');
            trashButton.addEventListener('click', async () => {
                const formData = new FormData();
                formData.append("csrf", CSRF_TOKEN);
                formData.append("path", path);
                formData.append("new-name", isTrash ? name.substring(".trash.".length) : `.trash.${name}`);
                await fetch('/files/rename', {method: 'POST', body: formData});
                location.reload();
            });
            tr.append(tdIconButton(trashButton));
        }
    }
});

// const uploadQueue = [];

// async function processQueue() {
//     const file = uploadQueue.shift();
//     console.debug('files: uploading file', file.name);

//     const formData = new FormData();
//     formData.append('csrf', document.getElementById('upload_csrf').value);
//     formData.append('dir', document.getElementById('upload_dir').value)
//     formData.append('upload', file);

//     const response = await fetch('/files/upload', {
//         method: 'POST',
//         body: formData,
//         redirect: 'manual',
//     });

//     if (!response.ok) {
//         console.warn('Error during upload, add to queue');
//         uploadQueue.push(file);
//     }

//     if (uploadQueue.length > 0) {
//         processQueue();
//     }
// }

// document.addEventListener('DOMContentLoaded', () => {
//     const dropzone = document.getElementById("dropzone");
//     dropzone.ondragenter = (event) => {
//         //event.stopPropagation();
//         event.preventDefault(); // must be called for dropzone to be a valid drop target
//         //dropzone.classList.add('hovering');
//         console.debug('files: ondragenter');
//     }

//     dropzone.ondragover = (event) => {
//         //event.stopPropagation();
//         event.preventDefault(); // must be called for dropzone to be a valid drop target
//         event.dataTransfer.dropEffect = 'copy';
//         console.debug('files: ondragover');
//     }

//     dropzone.ondragleave = () => {
//         dropzone.classList.remove('hovering');
//         console.debug('files: ondragleave');
//     }

//     dropzone.ondrop = async function(event) {
//         event.preventDefault(); // must be called to prevent default behaviour
//         dropzone.classList.remove('hovering');

//         console.debug('files: ondrop');

//         const files = event.dataTransfer.files;
//         console.debug('files: number of files', files.length);
//         for (const file of files) {
//             uploadFile(file);
//         }
//     }
// });
