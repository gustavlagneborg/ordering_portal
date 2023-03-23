function createKibanaLink() {
    var link = document.getElementById("data_link");
    link.setAttribute("href", "kibana.se")
    link.style.visibility = 'visible'
    link.style.display = "block"
}

function searchProjectTable() {
        // Declare variables
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("searchProjectInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("project-table");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }