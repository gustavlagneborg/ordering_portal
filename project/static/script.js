$(document).ready(function () {
    $('#projects_table').DataTable();
});

function createKibanaLink() {
    var link = document.getElementById("data_link");
    link.setAttribute("href", "kibana.se")
    link.style.visibility = 'visible'
    link.style.display = "block"
}