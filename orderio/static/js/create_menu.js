csrf = $("input[name='csrfmiddlewaretoken']").val();

$(document).on('click',"button[id^='add-btn']",function add(e){
    url = $(this).data("url")
    
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
        location.reload()
  
        
      },
      error: function(xhr,errmsg,err){

      },
      complete: function(){
        
      }
    });
  });
  $(document).on('click',"button[id^='del-btn']",function remove (e){
    url = $(this).data("url")
    $("#add-btn"+$(this).val()).text("Add");
    $("#add-btn"+$(this).val()).removeClass("disabled");
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
        $( "#menu-items" ).load(location.href + " #menu-items");
        location.reload($( "#dataTable" ));
        
      },
      error: function(xhr,errmsg,err){

      },
      complete: function(){
        
      }
    });
  });