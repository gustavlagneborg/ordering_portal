function validateProjectForm() {
    el = document.querySelector('.examination_form')
    button = document.querySelector(".toggle_visablility")

    var name = document.getElementById("project_name").value
    var delivery = document.getElementById("data_delivery").value

    if (delivery == "" || name == "")
    {
        alert("Please fill the required fields!")
    } else 
    {
        el.style.visibility = 'visible'
        el.style.display = "block"
        button.style.visibility = "hidden"
        button.style.display = "none"
    }
}

function validateExaminationForm() {
    var modality = document.getElementById("modalities").value
    var examinations = document.getElementById("examination").value
    submit_button = document.querySelector(".submit_button")
    kibana_link = document.querySelector(".kibana_link")

    if (examinations == "" || modality == "")
    {
        alert("Please fill the required fields!")
    } else 
    {
        submit_button.style.visibility = 'visible'
        submit_button.style.display = "block"
        kibana_link.style.visibility = 'visible'
        kibana_link.style.display = "block"
    }

}