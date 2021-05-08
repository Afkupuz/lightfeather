$( document ).ready(function() {
//On loading the page, load in data from the database
  $.ajax({ 
    type: "GET", 
    url: "/api/kanban",
  }).done(function(data) {
    data.forEach(element => {
      //Create a task for each element in the database
      create_task_card(element["column"], element["id"], element["body"], element["sort_order"], element["user"], element["modified"])
    });
  });

});

function create_task_card(column, new_id, new_text, sort_order, user, modified){
  //Create a task html element
  console.log(column + ", " + new_id + ", " + new_text + ", " + sort_order);
  var item = '<li id='+new_id+' data-sort-id='+sort_order+' class="task">';
  var input = '<p data-editable class="taskinput">'+new_text+'</p>';
  var edit = '<button class="update-button">Update</button>';
  var del = '<button class="delete-button">x</button>';
  var left = '<button class="left-button">\<</button>';
  var right = '<button class="right-button">\></button>';
  var time = new Date(modified)
  var date = '<p id="time">'+time.getMonth()+'/'+time.getDate()+'/'+time.getFullYear()+'</p>';
  var name = '<p id="user">'+user+'</p>';
  var close = '</li>';
  $('#'+column).append(item+input+edit+del+left+right+date+name+close);
}

function update_task(id, new_text, sort_order, column){
  //Update a task
  console.log("c" + column + ", i" + id + ", t" + new_text + ", o" + sort_order)
  $.ajax({ 
    type: "POST", 
    url: "/api/kanban",
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
        console.log("move")
        update_task(ui.item.data('task_id'), "", ui.item.data('sort_order'), ui.item.data('column'))
      },

    }).disableSelection();

    //Creates a new task
    $('.add-button').click(function() {
        $('.show-button').css({"visibility":"unset"})
        $('li#creation').css({"display":"none"})
        var new_text = $(this).closest(".task").find("p").html();
        $.ajax({ 
          type: "PUT", 
          url: "/api/kanban",
          data: {"text": new_text},
        }).done(function(ret) {
          create_task_card("backlog", ret["id"], new_text, 0, ret["user"], ret["date"])
        });
    });

    //Shows new task maker
    $('.show-button').click(function() {
      $(this).css({"visibility":"hidden"})
      $('li#creation').css({"display":"block"})
  });

    //Updates tasks
    $(document).on("click", ".update-button", function() {
      var task_id = $(this).closest(".task").attr("id");
      var new_text = $(this).closest(".task").find("p").html();
      console.log(task_id + new_text)
      console.log("update")
      update_task(task_id, new_text, "", "")
      $(this).css({"visibility": "hidden"})
    });

    //Deletes tasks
    $(document).on("click", ".delete-button", function() {
      var task_id = $(this).closest(".task").attr("id");
        $.ajax({ 
          type: "DELETE", 
          url: "/api/kanban",
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

      var $el = $(this);
              
      var $input = $('<input/>').val( $el.text() );
      $el.replaceWith( $input );
      
      var save = function(){
        var $p = $('<p data-editable class="taskinput" />').text( $input.val() );
        $input.replaceWith( $p );
      };

      $input.one('blur', save).focus();
      
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