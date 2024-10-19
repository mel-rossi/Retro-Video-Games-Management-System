function postRequestParams(link, params, runFunction, errorFunction) {
    let request = new XMLHttpRequest();
    request.open('POST', 'http://127.0.0.1:5000/' + link, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function () {
        let data = null;

        if (request.status >= 200 && request.status < 300) {
            data = JSON.parse(request.responseText);
            console.log('Response:', data);
            runFunction(data);
        }
        else {
            //assume we do not know the error
            data = { 
                'error': "Unknown error occured" 
            };

            //change data to known error message
            if (request.status == 404){            
                data = JSON.parse(request.responseText);
            }

            console.error('Request failed with status:', request.status);
            errorFunction(data);
        }
    };

    request.send(JSON.stringify(params));
}
