const INFO_DIV = document.getElementById('addInfo');
const MEMEMBER_ELEMENT = document.getElementById('memberInput');
const RESULT_CONTAINER = document.getElementById("resultInfo");

var confirmRentalStatus = false;
var videoGameID = NaN;
var memberID = NaN;

window.onload = () => {
    //member text box keydown when enter to call enterClick
    MEMEMBER_ELEMENT.onkeydown = (event) => {
        if(event.key == 'Enter'){
            enterClick();
        }

        if(!confirmRentalStatus){
            resultTextChange("");
        }
    };

    videoGameID = INFO_DIV.getAttribute("data-videogame-id");
};

function enterClick(){
    //if we are confirming to create the rental
    if(confirmRentalStatus){
        confirmRental();
    }
    //if we are not confirming rental grab member info
    else{
        //handles valid customer input with given textbox
        searchCustomer(MEMEMBER_ELEMENT, validCustomer, errorHandling);
    }
}

function validCustomer(data){
    confirmRentalStatus = true;

    memberID = data['Member'][0]['MemberID'];    

    let params = {
        'VideoGameID': videoGameID,
        'MemberID': memberID
    };

    postRequestParams('open_rental', params, 
        () => resultTextChange("Confirm rental for " + data['Member'][0]['FirstName'] + " " +  data['Member'][0]['LastName']), 
        errorHandling);
}

function confirmRental(){
    confirmRentalStatus = false;

    let params = {
        'Confirm': 'confirmed',
        'VideoGameID': videoGameID,
        'MemberID': memberID
    };

    postRequestParams('open_rental', params, ()=> resultTextChange("Rental Complete!"), errorHandling);
}

function resultTextChange(text){
    RESULT_CONTAINER.innerHTML = "";

    let thing = document.createElement("p");
    thing.innerText = text;

    RESULT_CONTAINER.appendChild(thing);
}

function errorHandling(errorData){
    resultTextChange(errorData['Error']);
}