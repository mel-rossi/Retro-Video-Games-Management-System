var currSearchOption = undefined;
var currStatusOption = undefined;

const GENRE_OPTIONS = [ "Sports", "Platformer/Racing", "Shooter", "Action/Adventure", "RPG", "Puzzle", "Adventure", "Simulation", "Strategy", "Fighting", "Racing" ];

//magic numbers from data set
const START_YEAR = 1977;
const END_YEAR = 2020;

//holds the values for textboxs with values and placeholders
const SEARCH_HOLDERS = { "title": ["", "Search games by title..."], "publisher": ["", "Search games by publisher..."] };
const YEAR_HOLDERS = { "startYear": [START_YEAR, "Start Year"], "endYear": [END_YEAR, "End Year"] };

//elements we dynamically change, only grab them once
const SEARCH_BAR_ELEMENT = document.getElementById("searchBar");
const START_YEAR_ELEMENT = document.getElementById("startYear");
const END_YEAR_ELEMENT = document.getElementById("endYear");
const SEARCH_FILTER_ELEMENT = document.getElementById("searchFilter");
const SEARCH_STATUS_ELEMENT = document.getElementById("statusFilter");
const SEARCH_GENRE_ELEMENT = document.getElementById("genreFilter");
const GAME_CARD_LIST_ELEMENT = document.getElementById("gameList");
const GAME_CONTAINER_ELEMENT = document.getElementById("gameContainer");
const SEARCH_CONTAINER_ELEMENT = document.getElementById("searchContainer");

window.onload = () => {
    //search container keydown check when enter to call search
    SEARCH_CONTAINER_ELEMENT.onkeydown = (event) => {        
        if (event.key == 'Enter') {            
            searchGames();
        }
    };

    currSearchOption = SEARCH_FILTER_ELEMENT.selectedOptions[0].id;
    currStatusOption = SEARCH_STATUS_ELEMENT.selectedOptions[0].id;

    createYearSearch();
    createGenreSelector(SEARCH_GENRE_ELEMENT);

    let scrollTimeout;

    GAME_CONTAINER_ELEMENT.addEventListener("scroll", () => {

        GAME_CONTAINER_ELEMENT.style.scrollbarColor = 'rgba(0, 0, 0, 0.5) rgba(0, 0, 0, 0.1)';

        clearTimeout(scrollTimeout);

        scrollTimeout = setTimeout(() => {
            GAME_CONTAINER_ELEMENT.style.scrollbarColor = 'transparent transparent';
            console.log('a');
        }, 1500);

    });
};

//create a start date and end date 
function createYearSearch() {
    createYearSelector(START_YEAR_ELEMENT, START_YEAR, END_YEAR);
    createYearSelector(END_YEAR_ELEMENT, START_YEAR, END_YEAR);
}

//create a year selector with a certain id and dates
function createYearSelector(element, startYear, endYear) {
    //Starting option with default value if nothing is selected
    let firstOption = document.createElement("option");
    firstOption.value = YEAR_HOLDERS[element.id][0];
    firstOption.innerText = YEAR_HOLDERS[element.id][1];
    element.appendChild(firstOption);

    //Generate year options based on start and end years
    for (let year = startYear; year <= endYear; year++) {
        let dateOption = document.createElement("option");
        dateOption.value = year;
        dateOption.innerText = year;

        element.appendChild(dateOption);
    }
}

function createGenreSelector(element){

    GENRE_OPTIONS.map((e) => {
        let option = document.createElement("option");
        option.value = e;
        option.innerText = e;
        element.appendChild(option); 
    });    
}

//function called when selection box's change value
function selectionChange(element) {
    if (element.id == "searchFilter") { //change for search type
        //set the previous search value to empty
        SEARCH_HOLDERS[currSearchOption][0] = "";

        //set the new search option (title/publisher)
        currSearchOption = element.selectedOptions[0].id;

        //change place holder for pretty
        SEARCH_BAR_ELEMENT.value = "";
        SEARCH_BAR_ELEMENT.setAttribute("placeholder", SEARCH_HOLDERS[currSearchOption][1]);
    }
    else if (element.id == "statusFilter") { //change for game status
        currStatusOption = element.selectedOptions[0].id;
    }
}

//when the search button is pressed
function searchGames() {
    const startYear = parseInt(START_YEAR_ELEMENT.value);
    const endYear = parseInt(END_YEAR_ELEMENT.value);

    SEARCH_HOLDERS[currSearchOption][0] = SEARCH_BAR_ELEMENT.value;

    //error handling for invalid start and end years
    if (startYear > endYear) {
        alert("End year must be greater than or equal to start year.")
        return;
    }

    let params = {
        //'option': "all_params",
        'title': SEARCH_HOLDERS["title"][0],
        'publisher': SEARCH_HOLDERS["publisher"][0],
        'start_year': startYear,
        'end_year': endYear,
        'status': currStatusOption,
        'genre' : 'RPG'
    };

    postRequestParams("search_game", params, generateGameCards, () => { });
}


//generate the game cards for what is given back from the post request
function generateGameCards(games) {
    //delete the old game cards if any
    deleteGameContainerValues();

    games.forEach(gameInfo => {
        addToGameContainer(gameInfo);
    });
}

//create a game card element with the given game information
function addToGameContainer(gameInfo) {
    let newGameCard = document.createElement("a");
    newGameCard.id = gameInfo.VideoGameID;
    newGameCard.setAttribute("class", "game-card");
    newGameCard.setAttribute("href", "gamestats?ID=" + gameInfo.VideoGameID);

    const appendElement = (tag, text) => {
        const element = document.createElement(tag);
        element.innerText = text;
        newGameCard.appendChild(element);
    };

    appendElement("h3", gameInfo.Title); //title    
    appendElement("p", "Id: " + gameInfo.VideoGameID); //video game id    
    appendElement("p", "Publisher: " + gameInfo.Publisher); //publisher   
    appendElement("p", "Genre: " + gameInfo.Genre) 
    appendElement("p", "Year: " + gameInfo.Year); //year
    appendElement("p", "Status: " + gameInfo.Availability); //status

    GAME_CARD_LIST_ELEMENT.appendChild(newGameCard);
}

//delete the game cards for when we do a new search
function deleteGameContainerValues() {
    //reset the html for the container
    GAME_CARD_LIST_ELEMENT.innerHTML = "";
}
