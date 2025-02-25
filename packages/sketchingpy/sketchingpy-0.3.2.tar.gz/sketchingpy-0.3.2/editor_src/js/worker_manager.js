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
