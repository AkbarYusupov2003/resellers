$( document ).ready(function() {

  $( ".delete-company" ).click(function() {
    var result = confirm("Компанияни очириб ташламохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        url: delete_company_url,
        type: 'DELETE',
        data: JSON.stringify({ company_pk: pk }),
        success: function(json){
          $("#card-admin-" + pk).remove();
        }
      });
    }
  });

  $( ".leave-company" ).click(function() {
    var result = confirm("Компаниядан чикиб кетмохчимисиз?");
    if (result) {
      pk = $(this).attr("data-pk");
      $.ajax({
        url: leave_company_url,
        type: 'DELETE',
        data: JSON.stringify({ company_pk: pk }),
        success: function(json){
          $("#card-agent-" + pk).remove();
        }
      });
    }
  });

});