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
          data: {"text": new_text},
        }).done(function(new_id) {
          $('#backlog').append('<li id='+new_id+' data-sort-id='+'1'+' class="task"><div><input type="text" class="taskinput" value="'+new_text+'"/><button class="update-button">Edit</button><button class="delete-button">Delete</button></div></li>');
        });
    });

    $('.get-button').click(function() {
      var id_val = $('#get_val').val() - 1;
      $.getJSON('/api/kanban', function(data) {
        $("#result").text("id: " + data[id_val]["id"] + " body: " + data[id_val]["body"]);
      });
    });

    $(document).on("click", ".update-button", function() {
      var task_id = $(this).closest(".task").attr("id");
      var new_text = $(this).closest(".task").find("input").val();
        $.ajax({ 
          type: "PUT", 
          url: "/task",
          data: {"task_id": task_id, "text": new_text} 
        });
    });

    $(document).on("click", ".delete-button", function() {
      var task_id = $(this).closest(".task").attr("id");
        $.ajax({ 
          type: "DELETE", 
          url: "/task",
          data: {"task_id": task_id} 
        }).done(function(thing) {
          $('li#'+task_id).remove();
        });
    });
    
});