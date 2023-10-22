$( document ).ready(function() {

  $( ".remove-supplier" ).click(function() {
    var result = confirm("Етказиб берувчини очирмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        type: 'DELETE',
        data: JSON.stringify({ supplier_pk: pk }),
        success: function(json){
          location.reload()
        }
      });
    }
  });

});