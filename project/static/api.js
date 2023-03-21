function login(username, password) {
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

  async function queryOrderingPortal() {
    const username = 'API_Admin';
    const password = 'apiadmin';
    const token = await login(username, password);
    return token;
    // // let token = localStorage.getItem('token'); // get the token from localStorage (or wherever it's stored)
    
    // // check if token is expired (assuming the token has an "exp" claim that specifies the expiration time)
    // const decodedToken = jwt_decode(token);
    // const expirationTime = decodedToken.exp * 1000; // convert expiration time to milliseconds
    // const isExpired = Date.now() >= expirationTime;
    
    // // if token is expired, refresh it with a new login request
    // if (isExpired) {
    //     const token = await login(username, password);
    //     console.log(token);
    //     return token;
    // }
    
  }

  async function getProjects() {

    const url = 'http://127.0.0.1:5000/api/v1/projects'; // replace with your API endpoint URL
    
    const headers = new Headers();
    const token = await queryOrderingPortal();
    headers.set('x-access-token', token); // set the JWT token in the x-access-token header
    
    const options = {
      method: 'GET',
      headers: headers
    };
    
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
    console.log(result) // "Some User token"
 })