var req = require('request')
var baseUrl = 'http://localhost:8000/';
var token = '';
const url = baseUrl + 'login/';

var loginData = require( './sisma.json');
const options = {
    method: 'post',
    body: loginData,
    json: true,
    url: url
  };
req.post( options, (e,r,b) => {
    if( e) {
        console.log( "Error");
        console.log(e);
    }
    console.log(b)
    if( b && b.data) {
        mydata = b.data;
        token = mydata.token.access;
        window.localStorage.setItem("token", token);
        console.log(token);
    }
})