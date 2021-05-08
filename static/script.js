$( document ).ready(function() {
  console.log( "ready!" );

  $.ajax({ 
    type: "GET", 
    url: "/api/kanban",
  }).done(function(data) {
    console.log("openning");
    data.forEach(element => {
      console.log("id: " + element["id"] + "column: " + element["column"] + "sort: " + element["sort_order"] + " body: " + element["body"]);
      create_task_card(element["column"], element["id"], element["body"], element["sort_order"])
    });
  });

});

function create_task_card(column, new_id, new_text, sort_order){
  $('#'+column).append('<li id='+new_id+' data-sort-id='+sort_order+' class="task"><div><input type="text" class="taskinput" value="'+new_text+'"/><button class="update-button">Edit</button><button class="delete-button">Delete</button></div></li>');
}

$(function() {
    $( ".sortable" ).sortable({
      connectWith: ".connectedSortable",
      receive: function( event, ui ) {
        $(this).css({"background-color":"blue"});
        $(ui.item).css({"background-color":"yellow"});
        var pos = ui.item.index();
        console.log("got moved " + pos)
      },
      update: function( event, ui ) {
        var pos = ui.item.index();
        console.log("got moved " + pos)
      },
      stop:function(event,ui){
        var prev = $(ui.item).prev.parent("ul").attr('id');
        var next = $(ui.item).next.parent("ul").attr('id');
        alert('prev = '+prev+' next = '+next);
    }
    }).disableSelection();

    $('.add-button').click(function() {
        var new_text = $('#new_text').val();
        $.ajax({ 
          type: "PUT", 
          url: "/api/kanban",
          data: {"text": new_text},
        }).done(function(new_id) {
          create_task_card("backlog", new_id, new_text, 0)
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

$(window).on("beforeunload", function() {
  console.log("closing")
  $.ajax({ 
    type: "GET", 
    url: "/cipher"
  });
})