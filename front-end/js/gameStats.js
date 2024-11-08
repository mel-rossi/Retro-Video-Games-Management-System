 // variables
 const GAME_CONTAINER_ELEMENT = document.getElementById('gameData');
 const TEXT_BOX_ELEMENT = document.getElementById('textBox'); 
 const RENTAL_HISTORY_CHART = document.getElementById('monthlyRentalChart').getContext('2d');
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

    const RENTAL_CHART = new Chart(RENTAL_HISTORY_CHART, {
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

    // Stats Text Box
    //like rank number, avg rental
    //Average Rental Time
    let averageRental = document.createElement("H3");
    averageRental.innerText = data['Average Rental'];
    TEXT_BOX_ELEMENT.appendChild(averageRental);

    //Ranking
    let rank_params = {
        'rank': 'game',
        'base': 'VideoGameID',
        'top': 'Default',
    }
    postRequestParams("rank", rank_params, getRank, () => { });

    function getRank(data){
        let rank = document.createElement("H3");
        rank.innerText = data['Ranked'][0]['Rank'];
        TEXT_BOX_ELEMENT.appendChild(rank);
    }
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
}
