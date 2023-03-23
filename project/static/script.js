function populateTable() {
    const table = document.getElementById('project-table2');
  
    // Create table headers
    const headers = ['Name', 'Age', 'City'];
    const headerRow = document.createElement('tr');
    for (let i = 0; i < headers.length; i++) {
      const th = document.createElement('th');
      th.textContent = headers[i];
      headerRow.appendChild(th);
    }
    
    // Add header row to the table head
    const tableHead = document.getElementById('project-header');
    tableHead.appendChild(headerRow);
    
    // Create table rows
    const data = [
      ['John', 25, 'New York'],
      ['Sarah', 30, 'Los Angeles'],
      ['Tom', 21, 'Chicago'],
      ['Emily', 27, 'San Francisco']
    ];
  
    // Add data rows to the table body
    const tableBody = document.getElementById('project-body');
    for (let i = 0; i < data.length; i++) {
      const row = document.createElement('tr');
      for (let j = 0; j < data[i].length; j++) {
        const cell = document.createElement('td');
        cell.textContent = data[i][j];
        row.appendChild(cell);
      }
      tableBody.appendChild(row);
    }
  }
  
  // Call the function to populate the table
  populateTable();

$(document).ready(function () {
    $('#projects_table2').DataTable();
});

function createKibanaLink() {
    var link = document.getElementById("data_link");
    link.setAttribute("href", "kibana.se")
    link.style.visibility = 'visible'
    link.style.display = "block"
}