const header = document.getElementById('headerText');
header.innerText = 'Think different Academy - School Buffet';
(async () => {
    header.innerText = await checkHealth() + ' - ' + header.innerText;
})();
