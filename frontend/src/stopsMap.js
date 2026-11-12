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
const searchInput = document.getElementById("stop-search");

// (async function () {
//     let stops = await getStops();
//     let stop = stops[0];
//     stop.image_url = "src/";
//     stop.name = "";
//     delete stop.id;
//     console.log(stop);
//     console.log(await createStop(stop));
// })();

async function initializeStops() {
    const stops = await getStops();
    renderStopImages(list, stops);
    searchInput.addEventListener("input", () => {
        renderStopImages(list, stops, searchInput.value);
    });
}

initializeStops();
