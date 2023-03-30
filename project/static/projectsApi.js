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
  headers.set('x-access-token', token) // set the JWT token in the x-access-token header
  const options = {
    method: method,
    headers: headers
  }

  return options
}

async function getProjects () {
  const url = 'http://127.0.0.1:5000/api/v1/projects'
  const options = await queryOrderingPortal('GET')
  console.log(options.headers)

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
          cell.textContent = project[key]
          var progressElement = document.createElement("progress")
          progressElement.id = 'project-progress'
          progressElement.max = 100

          // add progress bar
          if (project[key] === "Waiting for ethical approval") {
            progressElement.value = progressElement.max / 6
            progressElement.setAttribute("data-label", project[key])

          } else if (project[key] === "Ethical approval denied") {
            progressElement.value = (progressElement.max / 6) * 2
            progressElement.setAttribute("data-label", project[key])

          } else if (project[key] === "Ethical approval approved") {
            progressElement.value = (progressElement.max / 6) * 3
            progressElement.setAttribute("data-label", project[key])

          } else if (project[key] === "Retrieving data") {
            progressElement.value = (progressElement.max / 6) * 4
            progressElement.setAttribute("data-label", project[key])

          } else if (project[key] === "Uplaoding data") {
            progressElement.value = (progressElement.max / 6) * 5
            progressElement.setAttribute("data-label", project[key])

          } else if (project[key] === "Uploaded") {
            progressElement.value = (progressElement.max / 6) * 6
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
  })
})
