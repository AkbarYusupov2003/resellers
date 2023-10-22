$( document ).ready(function() {

  $( ".remove-category" ).click(function() {
    var result = confirm("Тоифалани очирмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ category_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});