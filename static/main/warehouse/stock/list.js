$( document ).ready(function() {

  $( ".remove-stock" ).click(function() {
    var result = confirm("Мавжуд махсулотни очирмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ stock_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});