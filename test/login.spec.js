require('jasmine-ajax')
var req = require('request')
var baseUrl = 'http://localhost:8000/';
var loginData = require( './sisma.json');


const pingtest = () => {
    this.msg = 'apple';
    this.url = [baseUrl, 'pingtest', this.msg].join('/');
    this.t = 0;
    this.getToken = () => {
        req.get(this.url, (e, r, b) => {
            this.t = 1;
            return b;
        })
    }
    
}

describe('Login', () => {
    xit('ping', () => {
        var l = pingtest;
        spyOn(l, 'getToken');
        expect(l.t).toEqual(1);
    })
    it('login1', () => {
        const url = baseUrl + 'login/';
        const options = {
            method: 'post',
            body: loginData,
            json: true,
            url: url
        };

        console.log(url);
        // var xmlhttp = XMLHttpRequest();
        req.post(options, (err, response, body) => {
            console.log(['error', error]);
            console.log(['sat', response]);
            if (body && body.data) {
                token = body.data.token.access;
                window.localStorage.setItem('token', token);
            }
        });
        console.log("helps");
        expect(1).toEqual(1);
    });
    it('emergency', () => {
        expect('a').toEqual('a');
    })
});

// describe( "clients", () => )