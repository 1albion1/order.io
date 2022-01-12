
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
            type: 'pie',
            data: {
            labels: data.labels,
            datasets: [{
                label: 'Amount',
                backgroundColor: 
                    data.bgColor
                  ,
                  
                  borderWidth: 1,
                
                data: data.data
            }]          
            },
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: 'Chart.js Pie Chart'
                }
              }
            },
        });
        
    }
  });
});

