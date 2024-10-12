function searchGames(){
    let searchOption = "publisher";
    let searchInput = "nin";

    let data = undefined;

    let params = {'option': searchOption, 'first_input': searchInput, 'second_input': ''}; //change this for each button click or somrthing        
    postRequestParams("search", params, goThroughGamesIDK);
}

function goThroughGamesIDK(games){
    games.forEach(gameInfo => {
        addToGameContainer(gameInfo);
    });
}

function addToGameContainer(gameInfo){
    let gameCardElement = undefined;
    let gameContainer = document.getElementById("gameList");

    let newGameCard = document.createElement("div");
    newGameCard.setAttribute("class","game-card");

    //title
    gameCardElement = document.createElement("h3");
    gameCardElement.innerText = gameInfo.Title;    
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