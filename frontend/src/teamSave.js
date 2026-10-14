const teamNameInput = document.getElementById("input-team-name");
const teamAddButton = document.getElementById("btn-addTeam");
const teammateInput = document.getElementById("input-teammates");

teamAddButton.addEventListener('click', async () => {
    const teamName = teamNameInput.value;
    const team = teammateInput.value;
    console.log( await createTeam(teamName, team.split("  ")));
})


const btnTeamLoad = document.getElementById("btn-load-teams");
const teamsTable = document.getElementById("teams");

btnTeamLoad.addEventListener('click', async () => {
    const teams = await getTeams();
    if (teams.length == 0) {
      teamsTable.innerHTML = "<p>No teams</p>";
      return;
    }
    const table = document.createElement("table");
    table.innerHTML = `
      <thead>
      <tr>
          <th>ID</th>
          <th>name</th>
          <th>team</th>
      </tr>
      </thead>`;

    const tbody = document.createElement("tbody");

    for (const t of teams) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
        <td>${t.id}</td>
        <td>${t.teamName}</td>
        <td>${t.teammates}</td>`;
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    teamsTable.replaceChildren(table);
})

const btnDelTeams = document.getElementById("btn-delete-teams");

btnDelTeams.addEventListener('click', async () => {
  await delTeams();
})
