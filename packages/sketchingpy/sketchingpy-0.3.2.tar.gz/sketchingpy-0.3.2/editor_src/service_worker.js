const pendingRequests = new Map();
const CACHE_NAME = "sketchbook-cache-202502241";

const requestsChannel = new BroadcastChannel("requests");
const responsesChannel = new BroadcastChannel("responses");

const EDITABLE_FILE_TYPES = [
    ".py",
    ".pyscript",
    ".txt",
    ".json",
    ".geojson",
    ".csv"
];

IMAGE_PRELOAD_TYPES = [".png", ".jpg", ".jpeg", ".gif", ".bmp"];

const PYSCRIPT_CONFIG = {
    "packages": ["http://localhost:8000/dist/sketchingpy-0.3.2-py3-none-any.whl"]
};

const OVERRIDE_FILES = [
    "index.html",
    "sketch.html",
    "service_worker.js",
    "file_worker.js",
    "fonts.css"
];


function getIsEditable(name) {
    const editableExtension = EDITABLE_FILE_TYPES.filter((x) => name.endsWith(x));
    return editableExtension.length != 0;
}


function getNakedPathName(request) {
    const url = new URL(request.url);
    const nakedPathName = url.pathname.replace("/", "");
    return nakedPathName;
}


function getIsSketch(request) {
    return getNakedPathName(request) === "sketch.html";
}


function getIsFontIntercept(request) {
    return getNakedPathName(request) === "fonts.css";
}


function getIsOverride(request) {
    const nakedPathName = getNakedPathName(request);
    return OVERRIDE_FILES.indexOf(nakedPathName) != -1;
}


function getRequiresNetwork(request) {
    const url = new URL(request.url);
    const nakedPathName = url.pathname.replace("/", "");
    const isIndex = url.pathname === "/";
    const isNested = url.pathname.substring(1, url.pathname.length).indexOf("/") != -1;
    const isOverride = getIsOverride(request);
    return isIndex || isNested || isOverride;
}


async function interceptRequest(request) {
    const url = new URL(request.url);
    const currentHost = self.location.hostname;

    const makeNetworkRequest = () => {
        return caches.open(CACHE_NAME).then((cache) => {
            const makeCachedRequest = () => {
                return fetch(request).then(async (networkResponse) => {
                    const isCurrentHost = url.hostname === currentHost;
                    const isResponseOk = networkResponse.ok;
                    const isGet = request.method === "GET";
                    if (isCurrentHost && isResponseOk && isGet) {
                        cache.put(url.pathname, networkResponse.clone());
                    }
                    return networkResponse;
                });
            }

            return cache.match(url.pathname).then((cachedValue) => {
                if (cachedValue !== undefined) {
                    return new Promise((resolve) => {
                        resolve(cachedValue);
                    });
                    makeCachedRequest();
                } else {
                    return makeCachedRequest();
                }
            });
        });
    }

    const getFilesRaw = () => {
        const filenamesFuture = manager.getItemNames();
        
        const networkFuture = makeNetworkRequest()
            .then((response) => response.text());

        return Promise.all([filenamesFuture, networkFuture]);
    }

    const isTtf = (x) => x.toLowerCase().endsWith("ttf");
    const isOtf = (x) => x.toLowerCase().endsWith("otf");
    const getFontName = (x) => x.replaceAll(".otf", "").replaceAll(".ttf", "");

    let future = null;
    if (currentHost !== url.hostname) {
        future = fetch(url.pathname).then(async (networkResponse) => {
            return networkResponse;
        });
    } else if (getIsSketch(request)) {
        const combinedFutures = getFilesRaw();

        future = combinedFutures.then((results) => {
            const filenames = results[0];
            const pageText = results[1];

            const filesObj = {};
            const filesStrs = [
                "\n[files]"
            ];
            filenames.forEach((filename) => {
                const src = "/" + filename;
                const dest = "./" + filename;
                filesStrs.push("\"" + src + "\" = \"" + dest + "\"");
            });
            const filesStr = filesStrs.join("\n");

            const fonts = filenames.filter((x) => isTtf(x) || isOtf(x));
            const fontNames = fonts.map(getFontName);
            const fontPreloads = fontNames.map((x) => {
                return "<li style='font-family: \"" + x + "\"'>" + x + "</li>";
            });
            const fontPreloadsStr = fontPreloads.join("\n");

            const images = filenames.filter((filename) => {
                const filenameLower = filename.toLowerCase();
                const matching = IMAGE_PRELOAD_TYPES.filter((x) => filenameLower.endsWith(x))
                const numMatching = matching.map((x) => 1).reduce((a, b) => a + b, 0);
                return numMatching > 0;
            });
            const imagePreloads = images.map((x) => {
                const preloadIdSuffix = x.replaceAll(".", "-").replaceAll(" ", "-");
                const preloadId = "preload-img-" + preloadIdSuffix;
                return "<li><img src='" + x + "' id='" + preloadId + "'></li>";
            });
            const imagePreloadsStr = imagePreloads.join("\n");

            const configObjStr = ([
                "interpreter = \"http://localhost:8000/third_party/pyodide/pyodide.mjs\"",
                "packages = " + JSON.stringify(PYSCRIPT_CONFIG["packages"]),
                
            ].join("\n")) + "\n" + filesStr;

            const sketchFile = url.searchParams.get("filename").replace("%20", " ");
            const epochTime = Date.now();
            const sketchFileCacheBuster = sketchFile + "?v=" + epochTime;

            return pageText.replaceAll("{{{ config }}}", configObjStr)
                .replaceAll("{{{ sketchFile }}}", sketchFileCacheBuster)
                .replaceAll("{{{ fontPreloads }}}", fontPreloadsStr)
                .replaceAll("{{{ imagePreloads }}}", imagePreloadsStr);
        }).then((content) => {
            const headers = {"headers": { "Content-Type": "text/html" }};
            return new Response(content, headers);
        });
    } else if (getIsFontIntercept(request)) {
        const combinedFutures = getFilesRaw();

        future = combinedFutures.then((results) => {
            const filenames = results[0];
            const cssTemplate = results[1];
            const epochTime = Date.now();
            
            const fonts = filenames.filter((x) => isTtf(x) || isOtf(x));
            const fontCode = fonts.map((font) => {
                const url = font;
                const name = getFontName(font);
                const typeDescription = isTtf(font) ? "truetype" : "opentype";
                return cssTemplate.replace("{{{ name }}}", name)
                    .replace("{{{ url }}}", url)
                    .replace("{{{ type }}}", typeDescription);
            });

            const fullCode = fontCode.join("\n\n");
            return fullCode;
        }).then((content) => {
            const headers = {"headers": { "Content-Type": "text/css" }};
            return new Response(content, headers);
        });
    } else if (getRequiresNetwork(request)) {
        future = makeNetworkRequest();
    } else {
        const effectiveUrl = url.pathname.replace("/", "");
        future = getItem(effectiveUrl).then((content) => {
            if (getIsEditable(effectiveUrl)) {
                return new Response(content);
            } else {
                return fetch(content)
                    .then((response) => response.blob())
                    .then((blob) => new Response(blob));
            }
        });
    }

    return (await future);
}


self.addEventListener("fetch", (event) => {
    const request = event.request;
    event.respondWith(interceptRequest(request));
});


class ReadOnlyOpfsFileManager {

    constructor() {
        const self = this;
        self._waitingPromises = new Map();

        responsesChannel.onmessage = (event) => {
            const data = event.data;
            const resolve = self._waitingPromises.get(data["target"]);
            self._waitingPromises.delete(data["target"]);
            if (resolve !== undefined) {
                resolve(data["content"]);
            } else if (data["filename"] !== "") {
                throw "Could not find resolve for " + data["filename"];
            }
        };
    }
    
    getItem(filename) {
        const self = this;
        const target = Date.now() + "." + filename.replace("%20", " ");

        return new Promise((resolve) => {
            self._waitingPromises.set(target, resolve);
            requestsChannel.postMessage({
                "filename": filename,
                "target": target
            });
        });
    }

    getItemNames() {
        const self = this;
        const target = Date.now() + ".";

        return new Promise((resolve) => {
            self._waitingPromises.set(target, resolve);
            requestsChannel.postMessage({
                "filename": "",
                "target": target
            });
        });
    }
    
}


const manager = new ReadOnlyOpfsFileManager();


function getItem(path) {
    return manager.getItem(path);
}
