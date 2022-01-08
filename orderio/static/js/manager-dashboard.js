
$(document).ready(function(){
    url = $('.chart-area').data("url");
  var $populationChart = $("#population-chart");
  labels = []
  defaultData = []
  $.ajax({
    method:"get",
    url: url,
    success: function (data) {
        var ctx = $populationChart;
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
            labels: data.labels,
            datasets: [{
                label: 'Number of orders',
               
                  borderColor: [
                    'rgba(13, 110, 253, 1)',
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
                text: 'Total orders each day (Pending or Accepted)' , 
            }
            }
        });
        
    }
  });
});

