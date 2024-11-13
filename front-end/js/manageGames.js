const MANAGE_CONTAINER = document.getElementById('manageContainer');

window.onload = () => {
    let id = MANAGE_CONTAINER.getAttribute("data-game-id");

    let manageState = MANAGE_CONTAINER.getAttribute("data-rental-state");

    if (manageState == "open"){
        new AddRental(MANAGE_CONTAINER, id).createAddRental();
    }
    else if(manageState == "close"){
        new RemoveRental(MANAGE_CONTAINER, id).createRemoveRental();
    }
    else{
        //do nothing I guess
    }
};
