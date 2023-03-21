async function login(username, password) {
    const url = "http://127.0.0.1:5000/api/v1/login"; // replace with your API endpoint URL
    
    const headers = new Headers();
    headers.set('Authorization', 'Basic ' + btoa(username + ':' + password)); // set the Authorization header using Basic authentication
    
    const options = {
      method: 'POST',
      headers: headers
    };
    
    return fetch(url, options)
      .then(response => {
        if (!response.ok) {
          throw new Error('Login failed');
        }
        return response.json();
      })
      .then(data => {
        const token = data.token; // replace with the name of the JWT token property returned by your API
        // do something with the token, such as storing it in localStorage or setting a cookie
        return token;
      })
      .catch(error => {
        console.error(error);
        // handle login error, such as displaying an error message to the user
      });
  }

async function queryOrderingPortal(method) {
    const username = 'API_Admin';
    const password = 'apiadmin';
    const token = await login(username, password);
    const headers = new Headers();

    headers.set('x-access-token', token); // set the JWT token in the x-access-token header
    const options = {
    method: method,
    headers: headers
    };

    return options;
}

async function getProjects() {
    const url = 'http://127.0.0.1:5000/api/v1/projects'; // replace with your API endpoint URL

    const options = await queryOrderingPortal("GET");

    return fetch(url, options)
    .then(response => {
    if (!response.ok) {
        throw new Error('Failed to get data');
    }
    return response.json();
    })
    .catch(error => {
    console.error(error);
    // handle error, such as displaying an error message to the user
    });
}


getProjects().then(data => {
  // Parse the JSON list of projects into a JavaScript object
  const projects = data.projects;

  // Create an HTML table element to display the projects
  const table = document.createElement('table');

  // Create the table header row
  const headerRow = document.createElement('tr');

  const projectKeys = Object.keys(projects[0]);
      projectKeys.forEach(key => {
      const header = document.createElement('th');
      header.textContent = key;
      headerRow.appendChild(header);
});
  // const nameHeader = document.createElement('th');
  // nameHeader.textContent = 'Project Name';
  // headerRow.appendChild(nameHeader);

  // const statusHeader = document.createElement('th');
  // statusHeader.textContent = 'Project Status';
  // headerRow.appendChild(statusHeader);

  // const pseudonymisationModel = document.createElement('th');
  // pseudonymisationModel.textContent = 'Pseudonymisation Model';
  // headerRow.appendChild(pseudonymisationModel);

  table.appendChild(headerRow);

  // Iterate through the list of projects and create table rows for each project
  // projects.forEach(project => {
  // const row = document.createElement('tr');
  
  // // add project name
  // const nameCell = document.createElement('td');
  // nameCell.textContent = project['Project name:'];
  // row.appendChild(nameCell);
  
  // // add project status
  // const statusCell = document.createElement('td');
  // statusCell.textContent = project['Project status:'];
  // row.appendChild(statusCell);

  // // add pseudo model
  // const pseudonymisationCell = document.createElement('td');
  // pseudonymisationCell.textContent = project['Pseudonymisation type:'];
  // row.appendChild(pseudonymisationCell);
  
  // table.appendChild(row);
  // });

  // Iterate through the list of projects and create table rows for each project
  projects.forEach(project => {
      const row = document.createElement('tr');
      projectKeys.forEach(key => {
          const cell = document.createElement('td');
          if (Array.isArray(project[key])) {
            project[key].forEach(list => {
              if (!cell.textContent) {
                cell.textContent += Object.values(list);
              } else {
                cell.textContent += ", ";
                cell.textContent += Object.values(list);
              }
            });
          } else {
            cell.textContent = project[key];
          }

          row.appendChild(cell);
      });
      table.appendChild(row);
  });

  // Get a reference to the div with ID "project-data"
  const projectDataDiv = document.getElementById('project-data1');

  // Add the table to the projectDataDiv element
  projectDataDiv.appendChild(table);

});


// getProjects().then(data => {
//   // Parse the JSON list of projects into a JavaScript object
//   const projects = data.projects;

//   // Create an HTML table element to display the projects
//   const table = document.createElement('table');

//   // Create the table header row
//   const headerRow = document.createElement('tr');

//   const nameHeader = document.createElement('th');
//   nameHeader.textContent = 'Project Name';
//   headerRow.appendChild(nameHeader);

//   const statusHeader = document.createElement('th');
//   statusHeader.textContent = 'Project Status';
//   headerRow.appendChild(statusHeader);

//   const pseudonymisationModel = document.createElement('th');
//   pseudonymisationModel.textContent = 'Pseudonymisation Model';
//   headerRow.appendChild(pseudonymisationModel);

//   table.appendChild(headerRow);

//   // Iterate through the list of projects and create table rows for each project
//   projects.forEach(project => {
//   const row = document.createElement('tr');
  
//   // add project name
//   const nameCell = document.createElement('td');
//   nameCell.textContent = project['Project name:'];
//   row.appendChild(nameCell);
  
//   // add project status
//   const statusCell = document.createElement('td');
//   statusCell.textContent = project['Project status:'];
//   row.appendChild(statusCell);

//   // add pseudo model
//   const pseudonymisationCell = document.createElement('td');
//   pseudonymisationCell.textContent = project['Pseudonymisation type:'];
//   row.appendChild(pseudonymisationCell);
  
//   table.appendChild(row);
//   });

//   // Get a reference to the div with ID "project-data"
//   const projectDataDiv = document.getElementById('project-data2');

//   // Add the table to the projectDataDiv element
//   projectDataDiv.appendChild(table);

// }).catch(error => {
//   alert(error);
// });