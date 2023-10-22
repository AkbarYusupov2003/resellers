$( document ).ready(function() {

  $( ".remove-user" ).click(function() {
    var result = confirm("Фойдаланувчини бушатмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ user_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});