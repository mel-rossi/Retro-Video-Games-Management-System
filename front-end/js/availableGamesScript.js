var searchOption = undefined;
var statusOption = undefined;

const START_YEAR = 1900;
const END_YEAR = 2100;

const SEARCH_FILTERS = ["title", "publisher", "year"];
const SEARCH_PLACEHOLDERS = {"title": "Search games by title...", "publisher": "Search games by publisher..."};

function bodyOnLoad(){
    searchOption = document.getElementById("searchFilter").selectedOptions[0].id;
    statusOption = document.getElementById("statusFilter").selectedOptions[0].id;

    //dynamically create textbox for searching
    document.getElementById("searchTypeContainer").appendChild(createGeneralSearch(SEARCH_FILTERS[0]));
}

//switch between the search type inputs
function searchSwitch(searchType){
    let searchElement = undefined;

    switch (searchType){
        case "title":            
        case "publisher":
            searchElement = createGeneralSearch(searchType);
            break;
        case "year":
            searchElement = createYearSearch();
            break;
        default:
            console.error("Invalid search switch occured")
            break;
    }

    return searchElement;
}

//create a general textbox for search
function createGeneralSearch(searchType){
    let searchBarElement = document.createElement("input");
    searchBarElement.setAttribute("type","text");
    searchBarElement.setAttribute("id", "searchBar");
    searchBarElement.setAttribute("placeholder", SEARCH_PLACEHOLDERS[searchType]);

    return searchBarElement;
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

function selectionChange(element){
    if(element.id == "searchFilter"){ 
        let searchBarElement = document.getElementById("searchBar");
        let newSearchElement = searchSwitch(document.getElementById("searchFilter").selectedOptions[0].id);

        searchBarElement.parentNode.replaceChild(newSearchElement, searchBarElement);    

        searchOption = element.selectedOptions[0].id;
    }
    else if(element.id == "statusFilter"){
        statusOption = element.selectedOptions[0].id;
    }    
}

function searchGames(){  
    let searchInput = undefined;    
    let searchBar = document.getElementById("searchBar");
    
    switch(searchBar.tagName){
        case "INPUT":
            //get the search value from the textbox
            searchInput = searchBar.value
            break;
        case "DIV":
            //child 0 is start date and child 1 is end date, get the selected option from each of them
            searchInput = [searchBar.children[0].selectedOptions[0].value, searchBar.children[1].selectedOptions[0].value];
            break;
    }

    let params = getSearchParams(searchInput);

    postRequestParams("search", params, goThroughGamesIDK);
}

function getSearchParams(searchInput){

    let params = {'option': searchOption, 'first_input': searchInput, 'status': statusOption};

    if(searchOption == "year"){
        params = {'option': searchOption, 'first_input': searchInput[0], 'second_input': searchInput[1], 'status': statusOption};
    }

    return params;
}

function goThroughGamesIDK(games){
    deleteGameContainerValues();

    games.forEach(gameInfo => {
        addToGameContainer(gameInfo);
    });
}

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

function deleteGameContainerValues(){
    let gameContainer = document.getElementById("gameList");
    let currGameCards = gameContainer.querySelectorAll("div");

    currGameCards.forEach(gameCard => gameCard.remove());
}