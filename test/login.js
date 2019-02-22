describe( 'Login', () => {
    it('login', () => {
        // var xmlhttp = XMLHttpRequest();

        var req = require( 'request')
        req('http://www.cnn.com/', ( error, response, body) => {
            console.log('error', error);
            console.log('sat', response);
            console.log('body', body);
        });
        console.log( "helps");
        expect(1).toEqual(1);
    });
    it( 'emeergency', () => {
        expect('a').toEqual('a');
    })
});

