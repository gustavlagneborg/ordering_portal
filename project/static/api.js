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


let projects = getProjects();
projects.then(function(result) {
    console.log(result)
 })