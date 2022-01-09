csrf = $("input[name='csrfmiddlewaretoken']").val();
$(document).on('click',"button[id^='add-btn']",function add(e){
    
    url = $(this).data("url");
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: url,
        data: {
          meal_id: $(this).val(),
          csrfmiddlewaretoken: csrf,
          action: 'add'
        },
        success: function (json){
            $( "#main" ).load(location.href + " #main");
          
        },
        error: function(xhr,errmsg,err){
  
        },
        complete: function(){
          
        }
      });

});

$(document).on('click',"button[id^='del-btn']",function remove (e){
    url = $(this).data("url")
    e.preventDefault();
    $.ajax({
      
      type: 'POST',
      url: url,
      data: {
        meal_id: $(this).val(),
        csrfmiddlewaretoken: csrf,
        action: 'remove'
      },
      success: function (json){
        $( "#main" ).load(location.href + " #main");
        
      },
      error: function(xhr,errmsg,err){

      },
      complete: function(){
        
      }
    });
  });