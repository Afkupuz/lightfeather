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
  var item = '<li id='+new_id+' data-sort-id='+sort_order+' class="task">'
  var input = '<div><p class="taskinput">'+new_text+'</p>'
  var edit = '<button class="update-button">Update</button>'
  var del = '<button class="delete-button">x</button>'
  var left = '<button class="left-button">\<</button>'
  var right = '<button class="right-button">\></button>'
  var close = '</div></li>'
  $('#'+column).append(item+input+edit+del+left+right+close);
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
      $(this).css({"visibility": "hidden"})
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

    //Left shift button
    $(document).on("click", ".left-button", function() {
      console.log("left")
      var old_column = $(this).closest("ul").attr("id");
      var task_id = $(this).closest(".task").attr("id");
      var new_column = "backlog"
      if (old_column == "complete") {
        new_column = "inprogress"
      };
      $('#'+new_column).append($('li#'+task_id));
      update_task(task_id, "", "", new_column);
    });
  
    //Righ shift button
    $(document).on("click", ".right-button", function() {
      console.log("right")
      var old_column = $(this).closest("ul").attr("id");
      var task_id = $(this).closest(".task").attr("id");
      console.log(old_column)
      var new_column = "complete"
      if (old_column == "backlog") {
        new_column = "inprogress"
      };
      $('#'+new_column).append($('li#'+task_id));
      update_task(task_id, "", "", new_column);
    });

    $(document).on('click', '.taskinput', function(){
      var task_id = $(this).closest(".task").attr("id");
      console.log(task_id)
      $('li#'+task_id+' .update-button').css({"visibility": "unset"})
      
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