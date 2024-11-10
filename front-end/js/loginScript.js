const LOGIN_BAR = document.getElementById("loginBar");

window.onload = () => {
    LOGIN_BAR.onkeydown = (event) => {
        if(event.key == 'Enter'){
            login();
        }
    };
};

function login(){
    let params = {
        'password': LOGIN_BAR.value
    }

    function worked(data){
        if (data['valid']){
            window.location.href = data['redirect_url'];
        }
        else{
            alert("bad");
        }
    }

    postRequestParams("/authenticator", params, worked, () => {});
}