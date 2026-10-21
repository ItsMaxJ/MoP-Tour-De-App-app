function renderStopsTable(container, stops) {
    if (stops.length === 0) {
        container.innerHTML = "<p>No stops</p>";
        return;
    }
    const table = document.createElement("table");

    const headers = Object.keys(stops[0])
    const headerRow = document.createElement("tr")

    for (const header of headers) {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    }
    const thead = document.createElement("thead");
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");

    for (const stop of stops) {
        const row = document.createElement("tr");
        for (const header of headers) {
            const cell = document.createElement("td");
            cell.textContent = stop[header];
            row.appendChild(cell);
        }

        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    container.replaceChildren(table);
}

const list = document.getElementById("stop-list");
(async () => {
    renderStopsTable(list, await getStops());
})();
