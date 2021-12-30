
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
                backgroundColor: 
                    'rgba(255, 99, 132, 0.2)'
                    
                  ,
                  borderColor: 
                    'rgb(255, 99, 132)'
                    
                  ,
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
                text: 'Amount spent by week for ' + $('#user-select option:selected').text(), 
            }
            }
        });
        
    }
  });
  myChart.destroy();  
});

