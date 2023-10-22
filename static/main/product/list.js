$( document ).ready(function() {

  $( ".remove-product" ).click(function() {
    var result = confirm("Махсулотни очирмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ product_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});