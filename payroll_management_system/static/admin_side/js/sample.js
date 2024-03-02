const searchInput = document.getElementById('searchInput');
const table = document.getElementById('myTable');
const rows = table.getElementsByTagName('tr');
const noResults = document.getElementById('noResults');
const checkAll = document.getElementById('checkAll');
const employeeCheckboxes = document.querySelectorAll('.employeeCheckbox');

checkAll.addEventListener('change', function() {
  employeeCheckboxes.forEach(function(checkbox) {
    if (checkbox.closest('tr').style.display !== 'none') {
      checkbox.checked = checkAll.checked;
    }
  });
});

searchInput.addEventListener('input', function() {
  const searchText = searchInput.value.toLowerCase();
  let showNoResults = true;
  let filteredRows = [];

  for (let i = 2; i < rows.length; i++) {
    let row = rows[i];
    let cells = row.getElementsByTagName('td');
    let found = false;

    for (let j = 0; j < cells.length; j++) {
      let cellText = cells[j].textContent.toLowerCase();
      if (cellText.includes(searchText)) {
        found = true;
        break;
      }
    }

    if (found) {
      row.style.display = '';
      filteredRows.push(row);
      showNoResults = false;
    } else {
      row.style.display = 'none';
    }
  }

  // Toggle visibility of noResults div based on showNoResults
  if (showNoResults) {
    noResults.style.display = 'block';
  } else {
    noResults.style.display = 'none';
  }

  // Update checkAll checkbox based on filtered rows
  if (filteredRows.length === 0) {
    checkAll.checked = false;
  } else {
    let allChecked = true;
    filteredRows.forEach(function(row) {
      let checkbox = row.querySelector('.employeeCheckbox');
      if (!checkbox.checked) {
        allChecked = false;
      }
    });
    checkAll.checked = allChecked;
  }
});

// Listen for changes in employee checkboxes
employeeCheckboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', function() {
    // If any employee checkbox is unchecked, uncheck the "checkAll" checkbox
    if (!this.checked) {
      checkAll.checked = false;
    } else {
      // Check if all filtered employee checkboxes are checked
      let allChecked = true;
      let filteredRows = table.querySelectorAll('tbody tr');
      filteredRows.forEach(function(row) {
        let checkbox = row.querySelector('.employeeCheckbox');
        if (!checkbox.checked) {
          allChecked = false;
        }
      });
      // If all filtered employee checkboxes are checked, check the "checkAll" checkbox
      checkAll.checked = allChecked;
    }
  });
});
