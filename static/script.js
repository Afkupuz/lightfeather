$(function() {
    $( ".sortable" ).sortable({
      connectWith: ".connectedSortable",
      receive: function( event, ui ) {
        $(this).css({"background-color":"blue"});
      }
    }).disableSelection();

    $('.add-button').click(function() {
        var txtNewItem = $('#new_text').val();
        $(this).closest('div.container').find('ul').append('<li class="task">'+txtNewItem+'</li>');
    });    
  });