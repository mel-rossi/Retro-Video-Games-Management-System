function postRequestParams(link, params, runFunction){    
    let request = new XMLHttpRequest();
    request.open('POST', 'http://localhost:5500/' + link, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function () {
        if (request.status >= 200 && request.status < 300) {
            let data = JSON.parse(request.responseText);             
            console.log('Response:', data);
            runFunction(data);
        } else {
            console.error('Request failed with status:', request.status);
        }
    };

    request.send(JSON.stringify(params));
}