const CORE_SRC = "/third_party/core.js?v=0.2.1";


function getSketchName() {
    const paramsStr = window.location.search;
    const params = new URLSearchParams(paramsStr);
    return params.get("filename");
}


function wrapConsole() {
    const originalConsole = window.console;
    const listHolder = document.getElementById("sketch-canvas-console");

    const buildElement = (message) => {
        const newElement = document.createElement("li");
        
        const messageClearAmp = message.replaceAll("&", "&amp;");
        const messageClearLt = messageClearAmp.replaceAll("<", "&lt;");
        const messageClearGt = messageClearLt.replaceAll(">", "&gt;");
        newElement.innerHTML = messageClearGt;
        
        return newElement;
    };  

    window.console = {
        debug: (message) => {
            originalConsole.debug(message);
            const newElement = buildElement(message);
            listHolder.appendChild(newElement);
        },
        log: (message) => {
            originalConsole.log(message);
            const newElement = buildElement(message);
            listHolder.appendChild(newElement);
        },
        info: (message) => {
            originalConsole.info(message);
            const newElement = buildElement(message);
            listHolder.appendChild(newElement);
        },
        warn: (message) => {
            originalConsole.warn(message);
            const newElement = buildElement(message);
            listHolder.appendChild(newElement);
        },
        error: (message) => {
            originalConsole.error(message);
            const newElement = buildElement(message);
            listHolder.appendChild(newElement);
        }
    };
}


function main() {
    const millis = Date.now();
    const sketchName = getSketchName();

    const sketchLabelText = document.createTextNode(sketchName);
    document.getElementById("sketch-label").appendChild(sketchLabelText);

    let progress = 0;
    const progressBar = document.getElementById("sketch-load-progress");
    progressBar.value = 0;
    const incrementBar = () => {
        progressBar.value += 1;

        if (progressBar.value < 19) {
            setTimeout(incrementBar, 500);
        }
    };
    incrementBar();

    wrapConsole();

    setTimeout(() => {
        const injectPoint = document.getElementById("sketch-inject");
        const path = document.getElementById("sketch-file").value;
        const tagSrc = "<script type=\"py\" src=\"" + path + "\"></script>";
        injectPoint.innerHTML = tagSrc;

        const fontsPreloader = document.getElementById("sketch-fonts-holder");
        fontsPreloader.style.display = "none";

        const imagesPreloader = document.getElementById("sketch-image-holder");
        imagesPreloader.style.display = "none";
    }, 100);
}


main();
