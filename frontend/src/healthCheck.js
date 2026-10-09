
const header = document.getElementById('headerText');
header.innerText = 'School Buffet';
(async () => {
    header.innerText = await checkHealth() + ' - ' + header.innerText;
})();
