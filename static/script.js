$(function() {
    $( ".sortable" ).sortable({
      connectWith: ".connectedSortable",
      receive: function( event, ui ) {
        $(this).css({"background-color":"blue"});
      }
    }).disableSelection();

    $('.add-button').click(function() {
        var new_text = $('#new_text').val();
        $.ajax({ 
          type: "PUT", 
          url: "/api/kanban",
          data: {"text": new_text} 
        });
        $(this).closest('div.container').find('ul').append('<li class="task">'+new_text+'</li>');
    });

    $('.get-button').click(function() {
      $.getJSON('/api/kanban', function(data) {
        $("#result").text("id: " + data[0]["id"] + " body: " + data[0]["body"]);
      });
    });

    $('.update-button').click(function() {
      var task_id = 1;
      var new_text = "one"
        $.ajax({ 
          type: "PUT", 
          url: "/task",
          data: {"task_id": task_id, "text": new_text} 
        });
    });
    
  });