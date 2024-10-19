   // Rental History (Line Chart)
   const ctx = document.getElementById('rentalHistoryChart').getContext('2d');
   const rentalHistoryChart = new Chart(ctx, {
       type: 'line',
       data: {
           labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
           datasets: [{
               label: 'Days Rented',
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

   // Inventory (Pie Chart)
   const inventoryCtx = document.getElementById('inventoryChart').getContext('2d');
   const inventoryChart = new Chart(inventoryCtx, {
       type: 'pie',
       data: {
           labels: ['In Stock', 'Rented'],
           datasets: [{
               data: [70,30], //Hardcoded inventory stats In stock 70, Rented 30
               backgroundColor: ['rgba(255, 99, 132, 20)', 'rgba(54, 162, 235, 20)'],
               /*backgroundColor:['#36a2eb','#ffcd56'],*/
               hoverOffset: 4
           }]
       },
       options: {
           responsive: true,
           plugins: {
               legend: {
                   position: 'top',
               }
           }
       }
   });

   // Rank Box

