function searchGames(){
    let searchOption = "publisher";
    let searchInput = "";

    var data = {'option': searchOption, 'first_input': searchInput, 'second_input': ''}; //change this for each button click or somrthing
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://localhost:5500/search', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 300) {
                    var response = JSON.parse(xhr.responseText); //change code to store it in a var or something idk
                    console.log('Response:', response);
                } else {
                    console.error('Request failed with status:', xhr.status);
                }
            };
            xhr.send(JSON.stringify(data));                     
}