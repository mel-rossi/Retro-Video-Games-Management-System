var currSearchOption = undefined;
var currStatusOption = undefined;

const START_YEAR = 1900;
const END_YEAR = 2100;

//holds the values for textboxs with values and placeholders
const SEARCH_HOLDERS = {"title": ["", "Search games by title..."], "publisher": ["", "Search games by publisher..."]};

const SEARCH_BAR_ELEMENT = document.getElementById("searchBar");

function bodyOnLoad(){
    currSearchOption = document.getElementById("searchFilter").selectedOptions[0].id;
    currStatusOption = document.getElementById("statusFilter").selectedOptions[0].id;
}

//create a start date and end date 
function createYearSearch(){
    let dateElement = document.createElement("div");
    dateElement.setAttribute("id","searchBar");

    let startDate = createYearSelector("startDate", START_YEAR, END_YEAR);
    let endDate = createYearSelector("endDate", START_YEAR, END_YEAR);    

    dateElement.appendChild(startDate);
    dateElement.appendChild(endDate);

    return dateElement;
}

//create a year selector with a certain id and dates
function createYearSelector(id, startYear, endYear){
    let yearSelector = document.createElement("select");
    yearSelector.setAttribute("id", id);       

    for(let year = startYear; year <= endYear; year++){
        let dateOption = document.createElement("option");        
        dateOption.value = year;
        dateOption.innerText = year;

        yearSelector.appendChild(dateOption);
    }    

    return yearSelector;
}

function searchTextChange(element){
    SEARCH_HOLDERS[currSearchOption][0] = element.value;
}

//function called when selection box's change value
function selectionChange(element){
    if(element.id == "searchFilter"){ //change for search type
        //set the previous search value to empty
        SEARCH_HOLDERS[currSearchOption][0] = "";

        //set the new search option (title/publisher)
        currSearchOption = element.selectedOptions[0].id;
        
        //change place holder for pretty
        SEARCH_BAR_ELEMENT.value = "";
        SEARCH_BAR_ELEMENT.setAttribute("placeholder", SEARCH_HOLDERS[currSearchOption][1]);        
    }
    else if(element.id == "statusFilter"){ //change for game status
        currStatusOption = element.selectedOptions[0].id;
    }    
}

//when the search button is pressed
function searchGames(){      
let test = getSearchParams();

    postRequestParams("search", test, generateGameCards);
}

//get the params for post request based on the search option
function getSearchParams(){
    
    let params = {'option': "all_params", 
        'title': SEARCH_HOLDERS["title"][0], 
        'publisher': SEARCH_HOLDERS["publisher"][0], 
        'start_year': '', 
        'end_year': '', 
        'status': currStatusOption
    };

    return params;
}

//generate the game cards for what is given back from the post request
function generateGameCards(games){
    //delete the old game cards if any
    deleteGameContainerValues();

    games.forEach(gameInfo => {
        addToGameContainer(gameInfo);
    });
}

//create a game card element with the given game information
function addToGameContainer(gameInfo){
    let gameCardElement = undefined;
    let gameContainer = document.getElementById("gameList");

    let newGameCard = document.createElement("div");
    newGameCard.id = gameInfo.VideoGameID;
    newGameCard.setAttribute("class","game-card");

    //title
    gameCardElement = document.createElement("h3");
    gameCardElement.innerText = gameInfo.Title;    
    newGameCard.appendChild(gameCardElement);

    //video game id
    gameCardElement = document.createElement("p");
    gameCardElement.innerText = "Id: " + gameInfo.VideoGameID;
    newGameCard.appendChild(gameCardElement);

    //publisher
    gameCardElement = document.createElement("p");
    gameCardElement.innerText = "Publisher: " + gameInfo.Publisher;
    newGameCard.appendChild(gameCardElement);

    //year
    gameCardElement = document.createElement("p");
    gameCardElement.innerText = "Year: " + gameInfo.Year;
    newGameCard.appendChild(gameCardElement);

    //status
    gameCardElement = document.createElement("p");
    gameCardElement.innerText = "Status: " + gameInfo.Availability;
    newGameCard.appendChild(gameCardElement);

    gameContainer.appendChild(newGameCard);
}

//delete the game cards for when we do a new search
function deleteGameContainerValues(){
    let gameContainer = document.getElementById("gameList");
    let currGameCards = gameContainer.querySelectorAll("div");

    currGameCards.forEach(gameCard => gameCard.remove());
}