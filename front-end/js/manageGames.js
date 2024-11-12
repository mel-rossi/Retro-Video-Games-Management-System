const MANAGE_CONTAINER = document.getElementById('manageContainer');

var videoGameID = NaN;
var memberID = NaN;

window.onload = () => {
    videoGameID = MANAGE_CONTAINER.getAttribute("data-videogame-id");

    let manageState = MANAGE_CONTAINER.getAttribute("rental-state");

    if (manageState == "open"){
        new AddRental(MANAGE_CONTAINER).createAddRental();
    }
    else if(manageState == "close"){

    }
    else{
        //do nothing I guess
    }
};
