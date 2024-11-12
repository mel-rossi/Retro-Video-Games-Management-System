// variables
const GAME_CONTAINER_ELEMENT = document.getElementById('gameData');
const TEXT_BOX_ELEMENT = document.getElementById('textBox'); 
const RENTAL_HISTORY_CHART = document.getElementById('monthlyRentalChart').getContext('2d');
const PERCENTAGE_TEXT = document.getElementById('percentageText'); 
const STATS_CONTAINER = document.getElementById('gameData');
const MONTHLY_RENTAL_CONTAINER = document.getElementById('monthlyRentalChart').getContext('2d');
const INVENTORY_ELEMENT = document.getElementById('inventoryChart').getContext('2d');
const TOTAL_VIDEO_GAMES = 1589;
 
// Get modal elements
const MODAL = document.getElementById("myModal");
const RENTAL_BUTTON = document.getElementById("rentButton");
const SPAN_MODAL = document.getElementsByClassName("close")[0];

// Open the modal when the button is clicked
RENTAL_BUTTON.onclick = function() {
    MODAL.style.display = "block";
}

// Close the modal when the 'x' is clicked
SPAN_MODAL.onclick = function() {
    MODAL.style.display = "none";
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target == MODAL) {
        MODAL.style.display = "none";
    }
}

 window.onload = game_stats_page;

 function game_stats_page() {
    let videoGameID = STATS_CONTAINER.getAttribute("data-videogame-id");
    
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
    postRequestParams("game_rental", inventory_params, generateInventoryChart, () => { });
    postRequestParams("rental_stat", rental_params, generateRentalChart, () => {});
    
 }
 
  // Rentals by Month (Bar Chart)
  function generateRentalChart(data){
    const RENTALS_BY_MONTH = data['Rentals by Month'];
    
    const MONTH_LABELS = [];
    const RENTAL_COUNTS = [];

    RENTALS_BY_MONTH.forEach((rentals) => {
        const MONTH = Object.keys(rentals)[0];
        const COUNT = rentals[MONTH];
        MONTH_LABELS.push(MONTH);
        RENTAL_COUNTS.push(COUNT);
    });

    const RENTAL_CHART = new Chart(MONTHLY_RENTAL_CONTAINER, {
        type: 'bar',
        data: {
            labels: MONTH_LABELS,
            datasets: [{
                label: 'Number of Rentals',
                data: RENTAL_COUNTS,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        stepSize: 1
                    }
                }
            }
        }
    });

  }
/* Inventory (Pie Chart) */
function generateInventoryChart(data){
    //load game title
    const GAME_TITLE = data['Video Game'][0]['Title'];
    document.getElementById('gameTitle').innerText = GAME_TITLE;
    
    //set current rentals to inventory
    let current_rentals;
    if (data['Rental Stats'] && data['Rental Stats'].length > 0){
        current_rentals = data['Rental Stats'][0]['Number of Copies Rented Out'];
    }
    else{
        current_rentals = 0; 
        //if rental stats is empty, default to 0
    }
   
    if (current_rentals === null || 
        current_rentals === undefined || 
        current_rentals === ""){
        current_rentals = 0; 
        //if current rentals is empty, default to 0
    }
   
    //load chart
    const INVENTORY = data['Video Game'][0]['Inventory'];
    const INVENTORY_CHART = new Chart(INVENTORY_ELEMENT, {
        type: 'pie',
        data: {
            labels: ['In Stock: ' + INVENTORY, 'Rented: ' + current_rentals],
            datasets: [{
                data: [INVENTORY-current_rentals, current_rentals], 
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

    /* Performance Summary */

    //Average Rental Time
    let averageHeader = document.getElementById("averageHeader");

    if (data && data ['Rental Stats'] 
        && Array.isArray(data['Rental Stats'])
        && data['Rental Stats'].length > 0){
        const RENTAL_STATS = data['Rental Stats'][0];

        if (RENTAL_STATS && RENTAL_STATS['Rental Time Average'] !== null 
            && RENTAL_STATS['Rental Time Average'] !== undefined 
            && RENTAL_STATS['Rental Time Average'] !== ""){
                averageHeader.innerText = `Average Rental Time: ${Math.round(RENTAL_STATS['Rental Time Average'])}`;    
            }
        else{
            averageHeader.innerText = "Average Rental Time: N/A";
        }
    }
    else {
        averageHeader.innerText = "Average Rental Time: N/A";
    }
    //averageHeader.innerText = `Average Rental Time: ${Math.round(data['Rental Stats'][0]['Rental Time Average'])}`;

    //Ranking
    let rank_params = {
        'rank': 'game',
        'base': 'VideoGameID',
        'top': ''
    }

    postRequestParams("rank", rank_params, getRank, () => { });
    function getRank(data){
        let videoGameID = STATS_CONTAINER.getAttribute("data-videogame-id");
        let rankHeader = document.getElementById("rankHeader");
        let videogameRank = data['Ranked'].find((item) =>item['VideoGameID'] == videoGameID);
        if (videogameRank){
            rankHeader.innerText = `Ranked #${videogameRank['Rank']}`;
        }
        else{
            rankHeader.innerText = "Rank not available";
        }
    }

}

function rentClick(){

}