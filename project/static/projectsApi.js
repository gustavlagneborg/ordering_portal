async function login (username, password) {
  const url = 'http://127.0.0.1:5000/api/v1/login' // replace with your API endpoint URL

  const headers = new Headers()
  headers.set('Authorization', 'Basic ' + btoa(username + ':' + password)) // set the Authorization header using Basic authentication

  const options = {
    method: 'POST',
    headers: headers
  }

  return fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Login failed')
      }
      return response.json()
    })
    .then(data => {
      const token = data.token // replace with the name of the JWT token property returned by your API
      // do something with the token, such as storing it in localStorage or setting a cookie
      return token
    })
    .catch(error => {
      console.error(error)
      // handle login error, such as displaying an error message to the user
    })
}

async function queryOrderingPortal (method) {
  const username = 'API_Admin'
  const password = 'apiadmin'
  const token = await login(username, password)
  const headers = new Headers()
  const options = {
    method: method,
    headers: headers
  }

  options.headers = {
    'Content-Type': 'application/json',
    'x-access-token': token
  };

  return options
}

async function getProjects () {
  const url = 'http://127.0.0.1:5000/api/v1/projects'
  const options = await queryOrderingPortal('GET')

  return fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to get data')
      }
      return response.json()
    })
    .catch(error => {
      console.error(error)
    })
}

function projectStructure (rawProject) {
  return {
    Project: rawProject['Project name'],
    User: rawProject['User'],
    Status: rawProject['Project status'],
    Pseudonymisation: rawProject['Pseudonymisation type'],
    'Data Deliveries': rawProject['Data Deliveries'],
    Modalities: rawProject['Modalities'],
    Examinations: rawProject['Examinations'],
    'Date ordered': rawProject['Date ordered'],
    id: rawProject['id'],
    'User id': rawProject['User id']
  }
}

function setProjectStatusProgress(cell, projectStatus) {  

  cell.textContent = projectStatus
  var progressElement = document.createElement("progress")
  progressElement.id = 'project-progress'
  progressElement.max = 100

  // add progress bar
  if (projectStatus === "Waiting for ethical approval") {
    progressElement.value = progressElement.max / 5
    progressElement.setAttribute("data-label", projectStatus)

  } else if (projectStatus === "Ethical approval approved") {
    progressElement.value = (progressElement.max / 5) * 2
    progressElement.setAttribute("data-label", projectStatus)

  } else if (projectStatus === "Retrieving data") {
    progressElement.value = (progressElement.max / 5) * 3
    progressElement.setAttribute("data-label", projectStatus)

  } else if (projectStatus === "Uploading data") {
    progressElement.value = (progressElement.max / 5) * 4
    progressElement.setAttribute("data-label", projectStatus)

  } else if (projectStatus === "Uploaded") {
    progressElement.value = (progressElement.max / 5) * 5
    progressElement.setAttribute("data-label", projectStatus)
  } else if (projectStatus === "Ethical approval denied") {
    progressElement.value = 0
    progressElement.setAttribute("data-label", projectStatus)
    cell.style.backgroundColor = "red"
  }
  cell.appendChild(document.createElement("br"))
  cell.appendChild(progressElement)

}


getProjects().then(data => {
  // Parse the JSON list of projects into a JavaScript object
  const rawProjects = data.projects

  // trim and re-order project
  const projects = []
  rawProjects.forEach(rawProject => {
    let project = projectStructure(rawProject)
    projects.push(project)
  })

  // Create an HTML table element to display the projects
  var thead = document.getElementById('projects-header')

  // Create the table header row
  const headerRow = document.createElement('tr')
  const projectKeys = Object.keys(projects[0])
  var count = 0

  projectKeys.forEach(key => {
    const header = document.createElement('th')

    header.id = key
    header.setAttribute('onclick', `sortTable(${count})`)

    count++
    if (key !== 'id' && key !== 'User id') {
      var sortLogo = document.createElement('i')
      sortLogo.className = 'fa-solid fa-sort'
      header.textContent = `${key} `
      header.appendChild(sortLogo)
      headerRow.appendChild(header)
    }
  })

  thead.appendChild(headerRow)

  // Iterate through the list of projects and create table rows for each project
  var tbody = document.getElementById('projects-body')

  projects.forEach(project => {
    const row = document.createElement('tr')

    projectKeys.forEach(key => {
      let cell = document.createElement('td')
      if (key !== 'id' && key !== 'User id') {
        if (Array.isArray(project[key])) {
          project[key].forEach(list => {
            if (!cell.textContent) {
              cell.textContent += Object.values(list)
            } else {
              cell.textContent += ', '
              cell.textContent += Object.values(list)
            }
          })
        } 
        else if (key === 'Project') {
          var link = document.createElement('a')
          link.href = `/projects/${project['id']}`

          var button = document.createElement('button')
          button.innerText = project[key]

          button.id = 'project-button'

          link.appendChild(button)
          cell.appendChild(link)
        } else if (key === 'User') {
          var link = document.createElement('a')
          link.href = `/users/${project['User id']}`

          var button = document.createElement('button')
          button.innerText = project[key]
          button.id = 'user-button'

          link.appendChild(button)
          cell.appendChild(link)
        } else if (key === 'Status') {
          setProjectStatusProgress(cell=cell, projectStatus=project[key])
        } else {
          cell.textContent = project[key]
        }
        row.appendChild(cell)
      }
    })
    tbody.append(row)
  })
})
