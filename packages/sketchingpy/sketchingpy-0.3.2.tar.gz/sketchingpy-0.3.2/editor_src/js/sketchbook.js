const EDITABLE_FILE_TYPES = [
    ".py",
    ".pyscript",
    ".txt",
    ".json",
    ".geojson",
    ".csv"
];

const PROJ_CONFIRM_MSG = [
    "Opening this project will cause your current project to be deleted from your browser.",
    "Be sure to export your current project before continuing.",
    "Do you want to continue?"
].join(" ");

const UPGRADE_MESSAGE = [
    "Project from the old editor found.",
    "Do you want to save it?",
    "Otherwise it will be deleted."
].join(" ");

const FAIL_START_MSG = [
    "The editor could not start.",
    "Maybe your browser is incompatible.",
    "Try updating!"
].join(" ");

const requestsChannel = new BroadcastChannel("requests");
const responsesChannel = new BroadcastChannel("responses");


function getIsEditable(name) {
    const editableExtension = EDITABLE_FILE_TYPES.filter((x) => name.endsWith(x));
    return editableExtension.length != 0;
}


class WorkerFileManager {

    constructor() {
        const self = this;
        self._messagePrefix = Date.now() + ":";
        self._messageCounter = 0;
        self._pendingPromises = new Map();

        self._fileWorker = new Worker("file_worker.js?v=0.2.1");
        self._fileWorker.addEventListener("message", (message) => {
            const data = message.data;
            const messageId = data["messageId"];
            const result = data["return"];

            const resolver = self._pendingPromises.get(messageId);
            resolver(result);
            self._pendingPromises.delete(messageId);
        });
    }

    _execute(method, filename, contents) {
        const self = this;
        
        const messageId = self._messagePrefix + self._messageCounter;
        self._messageCounter += 1;

        return new Promise((resolve) => {
            self._pendingPromises.set(messageId, resolve);
            self._fileWorker.postMessage({
                "messageId": messageId,
                "method": method,
                "filename": filename,
                "contents": contents
            });
        });
    }
    
    clearProject() {
        const self = this;
        return self._execute("clearProject", null, null);
    }
    
    loadProject(contents) {
        const self = this;
        return self._execute("loadProject", null, contents);
    }

    serializeProject() {
        const self = this;
        return self._execute("serializeProject", null, null);
    }
    
    getItemNames() {
        const self = this;
        return self._execute("getItemNames", null, null);
    }
    
    getItem(filename) {
        const self = this;
        return self._execute("getItem", filename, null);
    }
    
    updateItem(filename, contents) {
        const self = this;
        return self._execute("updateItem", filename, contents);
    }
    
    getMbUsed() {
        const self = this;
        return self._execute("getMbUsed", null, null);
    }
    
    createItem(filename) {
        const self = this;
        return self._execute("createItem", filename, null);
    }

    removeItem(filename) {
        const self = this;
        return self._execute("removeItem", filename, null);
    }

    migrate() {
        const self = this;
        return self._execute("migrate", null, null);
    }

}


class LocalStorageFileManager {
    
    clearProject() {
        const self = this;
        
        return new Promise((resolve) => {
            for (const [filename, content] of Object.entries(localStorage)) {
                localStorage.removeItem(filename);
            } 
        });
    }
    
    loadProject(contents) {
        const self = this;
        
        return new Promise((resolve) => {
            for (const [filename, content] of Object.entries(contents)) {
                self.updateFile(filename, content);
            }
            resolve(); 
        });
    }

    serializeProject() {
        const self = this;

        return new Promise((resolve) => {
            resolve(JSON.stringify(localStorage));
        });
    }
    
    getItemNames() {
        const self = this;
        
        return new Promise((resolve) => {
            resolve(Object.keys(localStorage));
        });
    }
    
    getItem(name) {
        const self = this;
        
        return new Promise((resolve) => {
            resolve(localStorage[name]);
        });
    }
    
    updateItem(name, contents) {
        const self = this;
        
        return new Promise((resolve) => {
            localStorage.setItem(filename, contents);
            resolve();
        })
    }
    
    getMbUsed() {
        const self = this;
        
        return self.getItemNames()
            .then((itemNames) => {
                const itemContentFutures = itemNames.map((itemName) => self.getItem(itemName));
                return Promise.all(itemContentFutures);
            })
            .then((contents) => {
                const totalSize = contents.map((x) => x.length).reduce((a, b) => a + b, 0);
                const totalKb = totalSize / 1024;
                const totalMb = totalKb / 1024;
                return totalMb;
            });
    }
    
    createItem(filename) {
        const self = this;
        
        return new Promise((resolve) => {
            if (localStorage.getItem(filename) === null) {
                localStorage.setItem(filename, "");
            }
            resolve();
        });
    }

    removeItem(filename) {
        const self = this;

        if (self._removePause) {
            self._removesWaiting.push(filename);
        } else {
            return new Promise((resolve) => {
                localStorage.removeItem(filename);
                resolve();
            });
        }
    }
    
}


class FilesListPresenter {

    constructor(rootDiv, sketchbookPresenter) {
        const self = this;

        self._rootDiv = rootDiv;
        self._sketchbookPresenter = sketchbookPresenter;
        self._selected = null;
    }

    setItems(newItems) {
        const self = this;

        newItems.sort();

        const sourceList = self._rootDiv.querySelector(".selection-list");
        sourceList.innerHTML = "";

        const newDivs = newItems.map((name) => {
            const newDiv = document.createElement("div");
            newDiv.classList.add("item");

            const newLink = document.createElement("a");
            newLink.href = "#" + name;
            newLink.classList.add("file-link");
            const newContent = document.createTextNode(name);
            newLink.appendChild(newContent);

            const delLink = document.createElement("a");
            delLink.href = "#" + name + "-delete";
            delLink.innerHTML = "delete";
            delLink.classList.add("del-link");

            newDiv.appendChild(newLink);
            newDiv.appendChild(delLink);

            const openFile = (event) => {
                event.preventDefault();
                event.stopPropagation();
                self._sketchbookPresenter.setFileOpen(name);
            };
            newLink.addEventListener("click", openFile);
            newDiv.addEventListener("click", openFile);

            delLink.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();
                self._sketchbookPresenter.deleteFile(name);
            });

            return newDiv;
        });

        newDivs.forEach((newDiv) => sourceList.appendChild(newDiv));

        self.setSelected(self.getSelected());
    }

    setSelected(newItem) {
        const self = this;

        const options = Array.of(...self._rootDiv.querySelectorAll(".item"));

        options.forEach((option) => {
            option.classList.remove("selected");
            option.ariaSelected = false;
        });

        if (newItem === null) {
            self._selected = null;
            return;
        }

        
        const isEditable = getIsEditable(newItem);
        if (!isEditable) {
            window.open("/" + newItem, '_blank');
            self._selected = null;
            return;
        }

        const matching = options.filter(
            (x) => x.querySelector(".file-link").innerHTML === newItem
        );
        if (matching.length == 0) {
            return;
        }

        matching[0].classList.add("selected");
        matching[0].ariaSelected = true;

        self._selected = newItem;
    }

    getSelected(newItem) {
        const self = this;
        return self._selected;
    }

}


class EditorPresenter {

    constructor(rootDiv, sketchbookPresenter) {
        const self = this;
        self._rootDiv = rootDiv;
        self._sketchbookPresenter = sketchbookPresenter;
        
        self._editor = ace.edit(rootDiv.id);
        self._editor.setOption("enableKeyboardAccessibility", true);
        self._editor.getSession().setMode("ace/mode/python");

        ace.config.set("basePath", "/third_party");
        ace.config.loadModule("ace/ext/searchbox");

        self._selected = null;

        setInterval(() => {
            self.save();
        }, 5000);
    }

    setContents(filename, content) {
        const self = this;
        self._editor.setValue(content);
        self._editor.clearSelection();
        self._selected = filename;
        document.getElementById("editor-holder").style.display = "block";
    }

    hide() {
        const self = this;
        document.getElementById("editor-holder").style.display = "none";
        self._selected = null;
    }

    save() {
        const self = this;
        
        if (self._selected === null) {
            return;
        }
        
        self._sketchbookPresenter.updateFile(self._selected, self._editor.getValue());
    }

    openFind() {
        const self = this;
        self._editor.execCommand("find");
    }

    openGoto() {
        const self = this;
        self._editor.execCommand("gotoline");
    }

    executeUndo() {
        const self = this;
        self._editor.execCommand("undo");
    }

    executeRedo() {
        const self = this;
        self._editor.execCommand("redo");
    }

}


const fileManager = new WorkerFileManager();


class SketchbookPresenter {

    constructor() {
        const self = this;

        self._sourcesList = new FilesListPresenter(document.getElementById("sources"), self);
        self._assetsList = new FilesListPresenter(document.getElementById("assets"), self);
        self._editor = new EditorPresenter(document.getElementById("editor"), self);
        self._fileManager = fileManager;

        const runButton = document.getElementById("run-button");
        runButton.addEventListener("click", (event) => {
            event.preventDefault();
            self._editor.save();
            setTimeout(() => {
                window.open(runButton.href, '_blank').focus();
            }, 100);
        });

        document.getElementById("search-button").addEventListener("click", (event) => {
            event.preventDefault();
            self._editor.openFind();
        });

        document.getElementById("goto-button").addEventListener("click", (event) => {
            event.preventDefault();
            self._editor.openGoto();
        });

        document.getElementById("undo-button").addEventListener("click", (event) => {
            event.preventDefault();
            self._editor.executeUndo();
        });

        document.getElementById("redo-button").addEventListener("click", (event) => {
            event.preventDefault();
            self._editor.executeRedo();
        });

        document.getElementById("new-button").addEventListener("click", (event) => {
            event.preventDefault();
            const newName = prompt("New filename:");
            if (newName === null) {
                return;
            }
            const newNameProper = newName.endsWith(".py") ? newName : newName + ".py";
            self.addNewFile(newNameProper);
        });

        const hiddenFileInput = document.getElementById("hidden-file-chooser");

        document.getElementById("upload-button").addEventListener("click", (event) => {
            event.preventDefault();
            hiddenFileInput.click();
        });

        document.getElementById("import-button").addEventListener("click", (event) => {
            event.preventDefault();
            hiddenFileInput.click();
        });

        hiddenFileInput.addEventListener("change", (event) => {
            event.preventDefault();
            const file = hiddenFileInput.files[0];
            const filename = file.name;

            const isEditable = getIsEditable(filename);

            if (filename.endsWith(".skprj")) {
                if (!confirm(PROJ_CONFIRM_MSG)) {
                    return;
                }

                file.text().then((contentsStr) => {
                    const contents = JSON.parse(contentsStr);

                    self._fileManager.clearProject()
                        .then(() => self._fileManager.loadProject(contents))
                        .then(() => self.refreshFilesList());
                });

                return;
            } else if (isEditable) {
                file.text().then((contents) => {
                    self.updateFileAndRefresh(filename, contents);
                });
            } else {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.addEventListener("load", () => {
                    const contents = reader.result;
                    self.updateFileAndRefresh(filename, contents);
                });
            }
        });

        document.getElementById("export-button").addEventListener("click", (event) => {
            self.exportProject();
        });

        self.refreshFilesList();
        self.setFileOpen(null);
    }

    refreshFilesList() {
        const self = this;

        const updateListsFuture = self._fileManager.getItemNames().then((itemNames) => {
            const sources = itemNames.filter((x) => x.endsWith(".py"));
            self._sourcesList.setItems(sources);

            const assets = itemNames.filter((x) => !x.endsWith(".py"));
            self._assetsList.setItems(assets);
        });
        
        const updateStorageUsed = self._fileManager.getMbUsed().then((totalMb) => {
            document.getElementById("current-usage").innerHTML = Math.round(totalMb * 10) / 10;
            document.getElementById("storage-bar").value = totalMb;
        });

        return Promise.all([updateListsFuture, updateStorageUsed]);
    }

    addNewFile(filename) {
        const self = this;

        return self._fileManager.createItem(filename).then(() => {
            self.refreshFilesList();
            self.setFileOpen(filename);
        });
    }

    setFileOpen(filename) {
        const self = this;

        self._editor.save();

        const updateEditor = () => {
            return new Promise((resolve) => {
                if (filename === null || !getIsEditable(filename)) {
                    self._editor.hide();
                    resolve();
                } else {
                    self._fileManager.getItem(filename).then((contents) => {
                        const runButton = document.getElementById("run-button");
                        runButton.href = "/sketch.html?filename=" + filename;
                        self._editor.setContents(filename, contents);
                        resolve();
                    });
                }
            })
        };

        const updateLists = () => {
            new Promise((resolve) => {
                self._sourcesList.setSelected(filename);
                self._assetsList.setSelected(filename);
                resolve();
            });
        };

        return updateEditor().then(updateLists);
    }

    updateFile(filename, contents) {
        const self = this;
        return self._fileManager.updateItem(filename, contents);
    }

    updateFileAndRefresh(filename, contents) {
        const self = this;
        self.updateFile(filename, contents).then(() => self.refreshFilesList());
    }

    deleteFile(filename) {
        const self = this;

        const updateFileSelected = () => {
            return new Promise((resolve) => {
                if (filename === self._sourcesList.getSelected()) {
                    self._sourcesList.setSelected(null);
                    self.setFileOpen(null).then(() => resolve());
                } else {
                    resolve();
                }
            });
        };
        
        const removeFile = () => {
            return new Promise((resolve) => {
                if (!confirm("Are you sure you want to remove this file?")) {
                    resolve();
                } else {
                    self._fileManager.removeItem(filename)
                        .then(() => {
                            return self.refreshFilesList();
                        })
                        .then(() => resolve());
                }
            })
            
        };

        return updateFileSelected().then(removeFile);
    }

    exportProject() {
        const self = this;

        const makeDownload = (newString) => {
            const newUrl = URL.createObjectURL(new Blob([newString]));

            const downloadLink = document.createElement("a");
            downloadLink.href = newUrl;
            downloadLink.download = "project.skprj";
            downloadLink.click();
        };

        return self._fileManager.serializeProject().then(makeDownload);
    }

}


function checkMigration() {
    const sourceFilesystem = new LocalStorageFileManager();
    sourceFilesystem.getItemNames().then((itemNames) => {
        if (itemNames.length == 0) {
            return;
        }
        
        if (confirm(UPGRADE_MESSAGE)) {
            const makeDownload = (newString) => {
                const newUrl = URL.createObjectURL(new Blob([newString]));

                const downloadLink = document.createElement("a");
                downloadLink.href = newUrl;
                downloadLink.download = "oldProject.skprj";
                downloadLink.click();
            };

            return sourceFilesystem.serializeProject().then(makeDownload);
        }

        sourceFilesystem.clearProject();
    });
}


function registerSaveCallback(sketchbook) {
    document.addEventListener('keydown', (event) => {
        const superModifierPressed = event.ctrlKey || event.metaKey;
        const sKeyPressed = event.key === 's'
        if (superModifierPressed && sKeyPressed) {
            event.preventDefault();
            sketchbook.save();
        }
    });

}


function main() {
    // Thanks MDN (CC0)
    // https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides
    try {
        navigator.serviceWorker.register("/service_worker.js", {
            scope: "/",
        }).then((registration) => {
            if (registration.installing) {
                console.log("Service worker installing");
            } else if (registration.waiting) {
                console.log("Service worker installed");
            } else if (registration.active) {
                console.log("Service worker active");
            }

            const sketchbook = new SketchbookPresenter();
            registerSaveCallback(sketchbook);

            checkMigration();
        });
    } catch (error) {
        alert(FAIL_START_MSG)
        console.log(error);
    }
}


requestsChannel.onmessage = (event) => {
    const data = event.data;
    const filename = data["filename"];

    if (filename === "") {
        fileManager.getItemNames().then((itemNames) => {
            responsesChannel.postMessage({
                "target": data["target"],
                "content": itemNames,
                "filename": filename
            });
        });
    } else {
        fileManager.getItem(filename).then((content) => {
            responsesChannel.postMessage({
                "target": data["target"],
                "content": content,
                "filename": filename
            });
        });
    }
};


main();
