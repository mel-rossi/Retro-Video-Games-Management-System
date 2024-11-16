const SEARCH_INPUT_ELEMENT = document.getElementById("searchInput");
const SEARCH_CONTAINER_ELEMENT = document.getElementById("searchContainer");
const CURRENT_RENTALS_ELEMENT = document.getElementById("currentRentals");
const PAST_RENTALS_ELEMENT = document.getElementById("pastRentals");
const RENTALS_CONTAINER_ELEMENT = document.getElementById("rentalResults");

// Get modal elements
const MODAL = document.getElementById("myModal");
const MODAL_IFRAME = document.getElementById('modalIframe');
const SPAN_MODAL = document.getElementsByClassName("close")[0];

const RENTAL_TYPES = {
    ACTIVE: 'Active Rentals',
    INACTIVE: 'Inactive Rentals',
    ERROR: 'Error'
};

const RENTAL_INFO = { [RENTAL_TYPES.ACTIVE]: CURRENT_RENTALS_ELEMENT, [RENTAL_TYPES.INACTIVE]: PAST_RENTALS_ELEMENT, [RENTAL_TYPES.ERROR]: CURRENT_RENTALS_ELEMENT };

// Close the modal when the 'x' is clicked
SPAN_MODAL.onclick = () => {
    MODAL.style.display = "none";
}

// Close the modal when clicking outside of the modal content
window.onclick = (event) => {
    if (event.target == MODAL) {
        MODAL.style.display = "none";
    }
}

window.onload = () => {
    //search container keydown check when enter to call search
    SEARCH_CONTAINER_ELEMENT.onkeydown = (event) => {
        if (event.key == 'Enter') {
            searchClick();
        }
    };

    let scrollTimeout;

    RENTALS_CONTAINER_ELEMENT.addEventListener("scroll", () => {
        RENTALS_CONTAINER_ELEMENT.style.scrollbarColor = 'rgba(0, 0, 0, 0.5) rgba(0, 0, 0, 0.1)';

        clearTimeout(scrollTimeout);

        scrollTimeout = setTimeout(() =>{
            RENTALS_CONTAINER_ELEMENT.style.scrollbarColor = 'transparent transparent';
            console.log('a');
        }, 1500);

    });
};

function searchClick(){
    searchCustomer(SEARCH_INPUT_ELEMENT, generateRentalCards, errorHandling);
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
    //clear containers for active & inactive
    deleteRentalContainerValues();

    //Add title for different rental status (active & inactive)
    RENTAL_INFO[RENTAL_TYPES.ACTIVE].appendChild(Object.assign(document.createElement("h3"), { innerText: "Currently Rented" }));
    RENTAL_INFO[RENTAL_TYPES.INACTIVE].appendChild(Object.assign(document.createElement("h3"), { innerText: "Past Rentals" }));

    //go through all the active games from the member
    //only show title and rented date
    customerData[RENTAL_TYPES.ACTIVE].forEach(rentedGame => {
        let cardDiv = addRentalCard(rentedGame, RENTAL_INFO[RENTAL_TYPES.ACTIVE], (appendElement) => {
            appendElement("p", "Game: ", rentedGame.Title);
            appendElement("p", "Rented on: ", new Date(rentedGame.StartDate).toDateString());            
        });

        cardDiv.onclick = () => {
            MODAL_IFRAME.setAttribute("src", "manage?ID=" + rentedGame.RentalID + "&M_State=close");
            MODAL.style.display = "block";
        };
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
    let newGameInfo = document.createElement("div");
    newGameInfo.id = rentedGame.RentalID;
    newGameInfo.setAttribute("class", "rental-card");

    let gameInfoFragment = document.createDocumentFragment();
    gameInfoFragment.appendChild(newGameInfo);

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

    gameElement.appendChild(gameInfoFragment);

    //return the game card div made
    return newGameInfo; 
}

function deleteRentalContainerValues() {
    for (let curr in RENTAL_INFO) {
        RENTAL_INFO[curr].innerHTML = "";
    }
}