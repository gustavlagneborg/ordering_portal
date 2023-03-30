async function login(username, password) {
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

async function queryOrderingPortal(method) {
  const username = 'API_Admin'
  const password = 'apiadmin'
  const token = await login(username, password)
  const headers = new Headers()
  headers.set('x-access-token', token) // set the JWT token in the x-access-token header
  const options = {
    method: method,
    headers: headers
  }

  return options
}

async function getProject(projectId) {
  const url = `http://127.0.0.1:5000/api/v1/projects/${projectId}`
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

function projectStructure(rawProject) {
  return {
    Project: rawProject['Project name'],
    User: rawProject['User'],
    Status: rawProject['Project status'],
    Pseudonymisation: rawProject['Pseudonymisation type'],
    'Data Deliveries': rawProject['Data Deliveries'],
    Modalities: rawProject['Modalities'],
    Examinations: rawProject['Examinations'],
    'Patient gender': rawProject['Patient gender'],
    'Date range': `${rawProject['Start date']} - ${rawProject['End date']}`,
    'Date ordered': rawProject['Date ordered'],
    'Age range': `${rawProject['Minimum patient age'] !== null
      ? rawProject['Minimum patient age']
      : ''
      } - ${rawProject['Maximum patient age'] !== null
        ? rawProject['Maximum patient age']
        : ''
      }`,
    Remittances: rawProject['Remittances'],
    'Producing departments': rawProject['Producing departments'],
    'Modality laboratories': rawProject['Modality laboratories'],
    'Radiology verdict': rawProject['Radiology verdict'],
    id: rawProject['id'],
    'User id': rawProject['User id']
  }
}


function loadProject(id) {

  getProject(id).then(rawProject => {
    let project = projectStructure(rawProject)
    const projectKeys = Object.keys(project)

    // Iterate through the list of projects and create table rows for each project
    var tbody = document.getElementById('project-body')
    const row = document.createElement('tr')

    projectKeys.forEach(key => {
      const cell = document.createElement('td')
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
        } else if (key === 'Status') {
          cell.textContent = project[key]
          var progressElement = document.createElement("progress")
          progressElement.id = 'project-progress'
          progressElement.max = 100

         // add progress bar
         if (project[key] === "Waiting for ethical approval") {
          progressElement.value = progressElement.max / 5
          progressElement.setAttribute("data-label", project[key])

        } else if (project[key] === "Ethical approval approved") {
          progressElement.value = (progressElement.max / 5) * 2
          progressElement.setAttribute("data-label", project[key])

        } else if (project[key] === "Retrieving data") {
          progressElement.value = (progressElement.max / 5) * 3
          progressElement.setAttribute("data-label", project[key])

        } else if (project[key] === "Uplaoding data") {
          progressElement.value = (progressElement.max / 5) * 4
          progressElement.setAttribute("data-label", project[key])

        } else if (project[key] === "Uploaded") {
          progressElement.value = (progressElement.max / 5) * 5
          progressElement.setAttribute("data-label", project[key])
        } else if (project[key] === "Ethical approval denied") {
          progressElement.value = 0
          progressElement.setAttribute("data-label", project[key])
        }
          cell.appendChild(document.createElement("br"))
          cell.appendChild(progressElement)

        } else {
          cell.textContent = project[key]
        }
        row.appendChild(cell)
      }
    })
    tbody.append(row)

    document.getElementById("project-h1").innerHTML = project["Project"]

  }).catch(error => {
    console.error(error);
  });
}


const currentPath = window.location.pathname;

// Extract the integer value from the URL path
const projectId = parseInt(currentPath.split('/').pop());

// Call the loadProject function with the project ID
loadProject(projectId);