// Filter performance and DJ roster based on search input and priority color checkboxes
document.getElementById('searchPerformance').addEventListener('input', function() {
    filterTable('performanceTable', this.value);
});

document.getElementById('searchDJ').addEventListener('input', function() {
    filterTable('djRoster', this.value);
});

document.getElementById('red').addEventListener('change', filterColors);
document.getElementById('yellow').addEventListener('change', filterColors);
document.getElementById('green').addEventListener('change', filterColors);
document.getElementById('blue').addEventListener('change', filterColors);

function filterTable(tableId, query) {
    let rows = document.querySelectorAll(`#${tableId} tr`);
    rows.forEach(row => {
        let text = row.textContent || row.innerText;
        row.style.display = text.includes(query) ? '' : 'none';
    });
}

function filterColors() {
    let selectedColors = [];
    if (document.getElementById('red').checked) selectedColors.push('Red');
    if (document.getElementById('yellow').checked) selectedColors.push('Yellow');
    if (document.getElementById('green').checked) selectedColors.push('Green');
    if (document.getElementById('blue').checked) selectedColors.push('Blue');

    let rows = document.querySelectorAll('#djRoster tr');
    rows.forEach(row => {
        let className = row.className;
        if (selectedColors.length === 0 || selectedColors.includes(className)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
