$( document ).ready(function() {
//On loading the page, load in data from the database
  $.ajax({ 
    type: "GET", 
    url: "/api/kanban",
  }).done(function(data) {
    data.forEach(element => {
      //Create a task for each element in the database
      create_task_card(element["column"], element["id"], element["body"], element["sort_order"])
    });
  });

});

function create_task_card(column, new_id, new_text, sort_order){
  //Create a task
  console.log(column + ", " + new_id + ", " + new_text + ", " + sort_order)
  $('#'+column).append('<li id='+new_id+' data-sort-id='+sort_order+' class="task"><div><input type="text" class="taskinput" value="'+new_text+'"/><button class="update-button">Edit</button><button class="delete-button">Delete</button></div></li>');
}

function update_task(id, new_text, sort_order, column){
  //Update a task
  console.log("c" + column + ", i" + id + ", t" + new_text + ", o" + sort_order)
  $.ajax({ 
    type: "PUT", 
    url: "/task",
    data: {"task_id": id, "body": new_text, "column": column, "sort_order": sort_order} 
  });
}

$(function() {
    //Handle the drag and drop functionality
    $( ".sortable" ).sortable({
      connectWith: ".connectedSortable",
      receive: function( event, ui ) {
        $(this).css({"background-color":"blue"});
        $(ui.item).css({"background-color":"yellow"});

        ui.item.data('task_id', ui.item.attr('id'));
        ui.item.data('sort_order', ui.item.index());
        ui.item.data('column', $(this).attr('id'));
      },
      update: function( event, ui ) {
        
        ui.item.data('task_id', ui.item.attr('id'));
        ui.item.data('sort_order', ui.item.index());
        ui.item.data('column', $(this).attr('id'));
    
      },
      stop: function( event, ui ) {
        update_task(ui.item.data('task_id'), "", ui.item.data('sort_order'), ui.item.data('column'))
      },

    }).disableSelection();

    //Creates a new task
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

    //Updates tasks
    $(document).on("click", ".update-button", function() {
      var task_id = $(this).closest(".task").attr("id");
      var new_text = $(this).closest(".task").find("input").val();
      update_task(task_id, new_text, "", "")
    });

    //Deletes tasks
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

//Refreshing or closing the page prompts a data backup
$(window).on("beforeunload", function() {
  console.log("closing")
  $.ajax({ 
    type: "GET", 
    url: "/cipher"
  });
})