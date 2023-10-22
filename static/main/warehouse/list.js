$( document ).ready(function() {

  $( ".remove-warehouse" ).click(function() {
    var result = confirm("Складни очирмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ warehouse_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});