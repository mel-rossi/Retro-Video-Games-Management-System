//regex for valid email & phone number
const regexEmail = new RegExp(/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/);
const regexPhone = new RegExp(/(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?/);

const SEARCH_INPUT_ELEMENT = document.getElementById("searchInput");
const SEARCH_CONTAINER_ELEMENT = document.getElementById("searchContainer");
const CURRENT_RENTALS_ELEMENT = document.getElementById("currentRentals");
const PAST_RENTALS_ELEMENT = document.getElementById("pastRentals");

const RENTAL_TYPES = {
    ACTIVE: 'active rentals',
    INACTIVE: 'inactive rentals',
    ERROR: 'error'
};

const RENTAL_INFO = { [RENTAL_TYPES.ACTIVE]: CURRENT_RENTALS_ELEMENT, [RENTAL_TYPES.INACTIVE]: PAST_RENTALS_ELEMENT, [RENTAL_TYPES.ERROR]: CURRENT_RENTALS_ELEMENT };

const INPUT_TYPES = Object.freeze({
    INVALID: -1,
    EMAIL: 0,
    PHONE: 1
});

window.onload = () => {
    //search container keydown check when enter to call search
    SEARCH_CONTAINER_ELEMENT.onkeydown = (event) => {
        if (event.key == 'Enter') {
            searchCustomer();
        }
    };
};

//return corresponding value to enum INPUT_TYPES for valid input
//returns an array [emum value, first match result]
function errorCheckInput(input) {
    //emails are lower case
    input = input.toLowerCase();
    const results = [regexEmail.exec(input), regexPhone.exec(input)];

    let validIndex = -1;
    for (let i = 0; i < results.length; i++) {
        if (results[i] != null) {
            validIndex = i;
            break;
        }
    }

    console.log(results[validIndex]);
    return [validIndex, validIndex == INPUT_TYPES.INVALID ? '' : results[validIndex][0]];
}

function searchCustomer() {
    let input = SEARCH_INPUT_ELEMENT.value;
    let errorResult = errorCheckInput(input);
    SEARCH_INPUT_ELEMENT.style.background = "";

    switch (errorResult[0]) {
        case INPUT_TYPES.INVALID:
            //set search to red when input bad...
            SEARCH_INPUT_ELEMENT.style.background = "#ffcfcf";
            return; //do not do an ajax call since invalid option
        case INPUT_TYPES.EMAIL:
            console.log("email");
            break;
        case INPUT_TYPES.PHONE:
            console.log("phone");
            break;
    }

    console.log(errorResult[1]);

    let params = { 'option': errorResult[1] };

    postRequestParams("member_rental", params, generateRentalCards, errorHandling);
}

function errorHandling(errorData) {
    //clear containers for rentals
    deleteRentalContainerValues();

    //create title for error message
    RENTAL_INFO[RENTAL_TYPES.ERROR].appendChild(Object.assign(document.createElement("h3"), { innerText: "Error Occured " }));

    //make a came card error message
    addRentalCard(errorData, RENTAL_INFO[RENTAL_TYPES.ERROR], (appendElement) => {
        appendElement("p", errorData[RENTAL_TYPES.ERROR], "");
    });
}

function generateRentalCards(customerData) {
    console.log(customerData);

    //clear containers for active & inactive
    deleteRentalContainerValues();

    //Add title for different rental status (active & inactive)
    RENTAL_INFO[RENTAL_TYPES.ACTIVE].appendChild(Object.assign(document.createElement("h3"), { innerText: "Currently Rented" }));
    RENTAL_INFO[RENTAL_TYPES.INACTIVE].appendChild(Object.assign(document.createElement("h3"), { innerText: "Past Rentals" }));

    //go through all the active games from the member
    //only show title and rented date
    customerData[RENTAL_TYPES.ACTIVE].forEach(rentedGame => {
        addRentalCard(rentedGame, RENTAL_INFO[RENTAL_TYPES.ACTIVE], (appendElement) => {
            appendElement("p", "Game: ", rentedGame.Title);
            appendElement("p", "Rented on: ", new Date(rentedGame.StartDate).toDateString());
        });
    });

    //go through all the inactive games from the member
    //only show title, rented date, and return date
    customerData[RENTAL_TYPES.INACTIVE].forEach(rentedGame => {
        addRentalCard(rentedGame, RENTAL_INFO[RENTAL_TYPES.INACTIVE], (appendElement) => {
            appendElement("p", "Game: ", rentedGame.Title);
            appendElement("p", "Rented on: ", new Date(rentedGame.StartDate).toDateString());
            appendElement("p", "Returned on: ", new Date(rentedGame.ReturnDate).toDateString());
        });
    });
}

function addRentalCard(rentedGame, gameElement, appendInfo) {
    console.log(rentedGame);

    let newGameInfo = document.createElement("div");
    newGameInfo.id = rentedGame.RentalID;
    newGameInfo.setAttribute("class", "rental-card");

    const appendElement = (tag, label, text) => {
        const element = document.createElement(tag);

        //strong label for subtitle in game card
        element.appendChild(Object.assign(document.createElement("strong"), { innerText: label }));

        //info of the corresponding label
        element.appendChild(document.createTextNode(text));

        newGameInfo.appendChild(element);
    };

    //call the passed information 
    appendInfo(appendElement);

    gameElement.appendChild(newGameInfo);
}

function deleteRentalContainerValues() {
    for (let curr in RENTAL_INFO) {
        RENTAL_INFO[curr].innerHTML = "";
    }
}