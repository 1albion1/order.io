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
        $(" #menu-items").load(" #menu-items")
        $("#add-btn"+json.id).addClass("disabled")
        
        if ($("#stuff").data("bl") >= ($("#stuff").data("mc")-1)){
          $("button[id^='add-btn']").prop('disabled', true);
        }
       
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
        $(" #menu-items").load(" #menu-items")
       $("#add-btn"+json.id).removeClass("disabled")
       if ($("#stuff").data("bl") <= ($("#stuff").data("mc"))){
        $("button[id^='add-btn']").prop('disabled', false);
      }
      },
      error: function(xhr,errmsg,err){

      },
      complete: function(){
        
      }
    });
  });