
$(document).on('change',"#user-select",function(){
    
    url = $('#user-select option:selected').data("url");
  var $populationChart = $("#population-chart");
  labels = []
  defaultData = []
  $.ajax({
    method:"get",
    url: url,
    success: function (data) {
        var ctx = $populationChart;
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
            labels: data.labels,
            datasets: [{
                label: 'Amount',
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(201, 203, 207, 0.2)'
                  ],
                  borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)',
                  ],
                  borderWidth: 1,
                
                data: data.data
            }]          
            },
            options: {
                
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Amount spent by department for ' + $('#user-select option:selected').text(), 
            }
            }
        });
        
    }
  });
  myChart.destroy();  
});

