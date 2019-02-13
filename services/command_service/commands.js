
const path = 'http://localhost:8083/commands';

$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();


    // upload data from server when doc is ready
    $.get(path)
      .done(function(response)
      {
        console.log( "success loading ");

        $.each( response, function( key, value ) {
          addRow(key, value);
        });
         addLastRow();
      })
      .fail(function()
      {
        console.log( "error loading" );
      });


    // Add row
    function addRow(question, answer) {
        var row = '<tr>' +
            '<td>' + question + '</td>' +
            '<td>' + answer+ '</td>' +
            '<td><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
        '</tr>';
        $("table").append(row);
        $('[data-toggle="tooltip"]').tooltip();
    }


	// Add last row
    function addLastRow() {
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="question" id="question"></td>' +
            '<td><input type="text" class="form-control" name="answer" id="answer"></td>' +
            '<td class="last-row"><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
        '</tr>';
        $("table").append(row);
        $('[data-toggle="tooltip"]').tooltip();
    }


	// Add row on add button click
	$(document).on("click", ".add", function(){
		var empty = false;
		var input = $(this).parents("tr").find('input[type="text"]');       // get input text

        input.each(function() {                                             // check if there are empty -> error
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});

		$(this).parents("tr").find(".error").first().focus();               // focus to the first inputText that is empty to write directly

		if(!empty)                                                         // if there's no errors then add item
		{
		    let button = this;
		    $.post(path, {'question': $('#question').val(), 'answer':$('#answer').val()})
              .done(function(response)
              {
                input.each(function(){
                    $(this).parent("td").html($(this).val());                   // replaces the inputText for the value entered
                });
                $(button).parents("tr").find(".add, .delete").toggle();
                $(button).parent("td").removeClass("last-row");
                addLastRow();

                console.log( "success adding");
              })
              .fail(function()
              {
                console.log( "error adding" );
              });
		}
    });


	// Delete row on delete button click
	$(document).on("click", ".delete", function()
	{
	    let button = this;
	    $.ajax({
            url: path,
            type: 'DELETE',
            data: {'question':$(this).parents("tr").find("td").first().html()},
            success: function(data) {
                console.log("succes deleting");

                $(button).parents("tr").remove();
            },
            error: function(err) {
                console.log(" error deleting ");
            }
        });
    });
});