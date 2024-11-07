 // variables
 const GAME_CONTAINER_ELEMENT = document.getElementById('gameData');
 const RANK_BOX_ELEMENT = document.getElementById('rankBox'); 
 const RENTAL_HISTORY_CHART = document.getElementById('rentalHistoryChart').getContext('2d');
 const PERCENTAGE_TEXT = document.getElementById('percentageText'); 
 const INVENTORY_ELEMENT = document.getElementById('inventoryChart').getContext('2d');
 const TOTAL_VIDEO_GAMES = 1589;
 

 window.onload = game_stats_page;

 function game_stats_page() {

    let videoGameID = GAME_CONTAINER_ELEMENT.getAttribute("data-videogame-id");

    let inventory_params = {
        'option': videoGameID,
        'out': 'stat'
    }
    let rental_params = {
        //'option': 'log',
        'id': videoGameID,
        'month_range': '',
        'year_range': ''
    }
    let rank_params = {
        'rank': 'game',
        'base': 'VideoGameID',
        'top': 'Default',
        //'trend': 'Default'
    }
    postRequestParams("game_rental", inventory_params, generateInventoryChart, () => { });
    //postRequestParams("rental_stat", history_params, collectingRentalStats, () => {});
    postRequestParams("rental_stat", rental_params, generateRentalChart, () => {});
    postRequestParams("rank", rank_params, generateRankBox, () => { });
 }
 
 var rentalStatsCounter = 0;
 var rentalHistoryData = {};
function collectingRentalStats(data){
    let firstKey = Object.keys(data)[0];

    rentalHistoryData[firstKey] = data[firstKey];
    rentalStatsCounter++;

    if(rentalStatsCounter == 2){
        console.log("got all the data");
        generateRentalChart(rentalHistoryData);
    }
}

  // Rental History (Line Chart)
  /* bar chart: how many times a game was rented that month */
function generateRentalChart(data){
    const RENTALS_BY_MONTH = data['Rentals by Month'];
    
    const MONTH_LABELS = [];
    const RENTAL_COUNTS = [];

    RENTALS_BY_MONTH.forEach((rentals) => {
        MONTH_LABELS.push(rentals);
        RENTAL_COUNTS.push(rentals['Count']);
    });

    //const RENTAL_AVERAGE = data['Rentals'][0]['Rental Stats'];
    const RENTAL_CHART = new Chart(RENTAL_HISTORY_CHART, {
    type: 'line',
    data: {
        labels: Object.keys(MONTH_LABELS),
        datasets: [{
            label: 'Number of Rentals',
            data: (Object.values(RENTAL_COUNTS)),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            pointBackgroundColor: '#ff5733',
            pointBorderColor: '#fff',
            pointRadius: 5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    });
}
// Inventory (Pie Chart)
function generateInventoryChart(data){
    const GAME_TITLE = data['Video Game'][0]['Title'];
    document.getElementById('gameTitle').innerText = GAME_TITLE;
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


   /* let percentage = document.createElement("p");
    const PERCENTAGE_VALUE = (CURR_RENTALS / INVENTORY) * 100
    percentage.innerText =  PERCENTAGE_VALUE.toFixed(0) + "% rented";
    PERCENTAGE_TEXT.appendChild(percentage);*/
    //INVENTORY_CHART.appendChild(percentage);

    //Alex WIP need to make 2 seperate canvases one for chart and one for text
    //Then draw them in the order you want to display them at
    /*const tempCanvas = document.createElement("canvas");
    const tempTextCanvas = tempCanvas.getContext("2d");

    //const percentageText = PERCENTAGE_VALUE.toFixed(0) + "% rented";
    
    tempCanvas.width = tempTextCanvas.measureText(percentageText).width + 20; //20 pixels for padding
    tempCanvas.height = 40;
    
    tempTextCanvas.textAlign = "center";
    tempTextCanvas.fillText(percentageText, tempCanvas.width / 2, tempCanvas.height / 2);
    
    INVENTORY_ELEMENT.drawImage(tempCanvas, tempCanvas.width, tempCanvas.height);*/
}
// Rank Box
function generateRankBox(data){
    let rank = document.createElement("H3");
    rank.innerText = data['Ranked'][0]['Rank'];
    RANK_BOX_ELEMENT.appendChild(rank);
}

