var searchOption = undefined

function bodyOnLoad(){
    searchOption = document.getElementById("searchFilter").value;
}

function selectionChange(){
    searchOption = document.getElementById("searchFilter").value;
}

function searchGames(){    
    let searchInput = document.getElementById("searchBar").value;

    let params = {'option': searchOption, 'first_input': searchInput, 'second_input': ''}; //change this for each button click or somrthing        
    postRequestParams("search", params, goThroughGamesIDK);
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