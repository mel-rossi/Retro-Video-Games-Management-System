//regex for valid email & phone number
const regexEmail = new RegExp(/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/);
const regexPhone = new RegExp(/(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?/);

const SEARCH_INPUT_ELEMENT = document.getElementById("searchInput");

const INPUT_TYPES = Object.freeze({
    INVALID: -1,
    EMAIL: 0,
    PHONE: 1
});

function bodyOnLoad(){
        
}

//return corresponding value to enum INPUT_TYPES for valid input
//returns an array [emum value, first match result]
function errorCheckInput(input){    
    const results = [regexEmail.exec(input), regexPhone.exec(input)];
    
    let validIndex = -1;
    for(let i = 0; i < results.length; i++){
        if(results[i] != null){
            validIndex = i;
            break;
        }
    }
    
    console.log(results[validIndex]);
    return [validIndex, validIndex == INPUT_TYPES.INVALID ? '' : results[validIndex][0]];
}

function searchCustomer(){
    //TODO: figure out if email or phone number
    let input = SEARCH_INPUT_ELEMENT.value;
    let errorResult = errorCheckInput(input);

    switch(errorResult[0]){
        case INPUT_TYPES.INVALID:
            console.error("Invalid input do nothing");
            return;            
        case INPUT_TYPES.EMAIL:
            console.log("email");
            break;
        case INPUT_TYPES.PHONE:
            console.log("phone");
            break;
    }

    console.log(errorResult[1]);

    let params = {'option': errorResult[1]};

    postRequestParams("search_member", params, generateRentalCards);
}

function generateRentalCards(data){
    console.log(data);
}