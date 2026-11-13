function renderStopImages(container, stops, query = "") {
    const normalizedQuery = query.trim().toLocaleLowerCase();
    const matchingStops = stops.filter(stop =>
        stop.name.toLocaleLowerCase().includes(normalizedQuery)
    );

    container.replaceChildren();
    if (matchingStops.length === 0) {
        container.textContent = normalizedQuery ? "No stops found" : "No stops";
        return;
    }
    for (const stop of matchingStops) {
        const a = document.createElement("a");
        const img = document.createElement("img");
        img.src = stop.image_url;
        img.alt = "stop image";
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
            const url = new URL(window.location.href);
            url.searchParams.set("id", stop.id);
            history.pushState({}, "", url);
            window.location.reload();
        });

        container.appendChild(a);
    }
}

async function loadStop(id) {
    const stop = await getStop(id);
    stopDetails.replaceChildren();
    stopDetails.style.display = "flex";stopDetails.style.gap = "5px";stopDetails.style.alignItems = "flex-start";
    const img = document.createElement("img");
    img.src = stop.image_url;
    img.style.width = "50%";
    img.style.objectFit = "cover";
    stopDetails.appendChild(img);
    const textContainer = document.createElement("div");
    textContainer.style.flex = "1";
    for (const [key, value] of Object.entries(stop)) {
        const p = document.createElement("p");
        p.innerText = `${key}: ${value}`;
        textContainer.appendChild(p);
    }
    stopDetails.appendChild(textContainer);
}

const stopDetails = document.getElementById("stop-details");
const list = document.getElementById("stop-list");
const searchInput = document.getElementById("stop-search");
const stopsListView = document.getElementById("stops-list-view");

async function initializeStops() {
    const stops = await getStops();
    renderStopImages(list, stops);
    searchInput.addEventListener("input", () => {
        renderStopImages(list, stops, searchInput.value);
    });
}

const params = new URLSearchParams(window.location.search);const stopId = Number(params.get("id"));
if (stopId) {
    stopsListView.hidden = true;
    loadStop(stopId);
}
else {
    stopsListView.hidden = false;
    initializeStops();
}
