function renderStopImages(container, stops) {
    if (stops.length === 0) {
        container.innerHTML = "no stops";
        return;
    }
    container.replaceChildren();
    for (const stop of stops) {
        const a = document.createElement("a");
        const img = document.createElement("img");
        img.src = stop.image_url;
        img.alt = stop.name
        a.appendChild(img);
        const name = document.createElement("p");
        name.innerText = stop.name;
        name.style.fontWeight = 700;
        name.style.textAlign = "center";
        name.style.marginTop = "4px";
        name.style.marginBottom = "7px";
        a.appendChild(name);
        a.style.cursor = "pointer";
        
        a.addEventListener("click", async () => {
            stopDetails.replaceChildren();
            for (const [key, value] of Object.entries(stop)) {
                const p = document.createElement("p");
                p.innerText = `${key}: ${value}`;
                stopDetails.appendChild(p);
            }
        });

        container.appendChild(a);
    }
}

const stopDetails = document.getElementById("stop-details");
const list = document.getElementById("stop-list");
(async () => {
    renderStopImages(list, await getStops());
})();
