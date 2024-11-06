 // variables
 const GAME_CONTAINER_ELEMENT = document.getElementById('gameData');
 const RANK_BOX_ELEMENT = document.getElementById('rankBox'); 
 const AVG_RENTAL_ELEMENT = document.getElementById('rentalHistoryChart').getContext('2d');
 const PERCENTAGE_TEXT = document.getElementById('percentageText'); 
 const INVENTORY_ELEMENT = document.getElementById('inventoryChart').getContext('2d');
 const TOTAL_VIDEO_GAMES = 1589;
 

 window.onload = game_stats_page;

 function game_stats_page() {

    let videoGameID = GAME_CONTAINER_ELEMENT.getAttribute("data-videogame-id");

    let rental_params = {
        'option': videoGameID,
        'out': 'stat'
    }
    let rank_params = {
        'rank': 'game',
        'base': 'VideoGameID',
        'top': 'Default',
        //'trend': 'Default'
    }
    postRequestParams("game_rental", rental_params, generateInventoryChart, () => { });
    postRequestParams("game_rental", rental_params, generateRentalChart, () => { });
    postRequestParams("rank", rank_params, generateRankBox, () => { });
 }
 
  // Rental History (Line Chart)
  /* bar chart: how many times a game was rented that month */
function generateRentalChart(data){
    const GAME_TITLE = data['Video Game'][0]['Title'];
    document.getElementById('gameTitle').innerText = GAME_TITLE;
    const RENTAL_AVERAGE = data['Rental Stats'][0]['Rental Time Average'];
    const RENTAL_CHART = new Chart(AVG_RENTAL_ELEMENT, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: "Average: " + RENTAL_AVERAGE.toFixed(0) + " Days",
            data: [5, 10, 15, 7, 10, 20, 5, 2, 15, 18, 20, 22],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            pointBackgroundColor: '#ff5733',
            pointBorderColor: '#fff',
            pointRadius: 5
        }]       
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 30,
            }
        }
    }

});
}


// Inventory (Pie Chart)
function generateInventoryChart(data){
    const CURR_RENTALS = data['Rental Stats'][0]['Number of Copies Rented Out'];
    const INVENTORY = data['Video Game'][0]['Inventory'];
    const INVENTORY_CHART = new Chart(INVENTORY_ELEMENT, {
        type: 'pie',
        data: {
            labels: ['In Stock: ' + INVENTORY, 'Rented: ' + CURR_RENTALS],
            datasets: [{
                data: [INVENTORY, CURR_RENTALS], 
                backgroundColor: ['rgba(54, 162, 235, 20)','rgba(255, 99, 132, 20)'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            }
        }
    });


    let percentage = document.createElement("p");
    const PERCENTAGE_VALUE = (CURR_RENTALS / INVENTORY) * 100
    percentage.innerText =  PERCENTAGE_VALUE.toFixed(0) + "% rented";
    PERCENTAGE_TEXT.appendChild(percentage);
    //INVENTORY_CHART.appendChild(percentage);

    //Alex WIP need to make 2 seperate canvases one for chart and one for text
    //Then draw them in the order you want to display them at
    const tempCanvas = document.createElement("canvas");
    const tempTextCanvas = tempCanvas.getContext("2d");

    const percentageText = PERCENTAGE_VALUE.toFixed(0) + "% rented";
    
    tempCanvas.width = tempTextCanvas.measureText(percentageText).width + 20; //20 pixels for padding
    tempCanvas.height = 40;
    
    tempTextCanvas.textAlign = "center";
    tempTextCanvas.fillText(percentageText, tempCanvas.width / 2, tempCanvas.height / 2);
    
    INVENTORY_ELEMENT.drawImage(tempCanvas, tempCanvas.width, tempCanvas.height);
}
// Rank Box
function generateRankBox(data){
    let rank = document.createElement("H3");
    rank.innerText = data['VideoGameID'][0]['Rank'];
    RANK_BOX_ELEMENT.appendChild(rank);
}

