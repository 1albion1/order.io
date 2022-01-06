go_to_url = "";
  $(document).on('click',"button[id^='del-btn']",function(){
    go_to_url = $(this).val()
  });

  $(document).on('click',"button[id^='approve-btn']",function(){
    go_to_url = $(this).val()
  });

  $(document).on('click',"#conf-btn",function(){
    document.location.href = go_to_url;
  });