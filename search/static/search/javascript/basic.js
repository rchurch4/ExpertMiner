var queries = [];
var starting_arg_string = "<button type='button' class='term' name='0'>Reset</button> or Click to Remove: ";
var arg_string = starting_arg_string;

$(document).ready(function () {

	// Add a term to the query when "Add" button is clicked
	$("#add_button").click(function (event) {
		// Gets the text from the form object
		var input = $("#query").val();
		// Checks to see if the input is valid
		if (input.length > 0 && input != "" && input != " " && input != "-1") {
			// Checks to see if the term has already been added
			if (queries.indexOf(input) == -1) {
				// Checks to see whether there are already terms in the query. If not, adds the Reset button to the beginning of the HTML
				if (queries.length == 0) {
					arg_string = starting_arg_string;
				}
				// Adds the newest term to the query
				queries[queries.length] = input;
				// Adds a button corresponding to the newest term to the HTML
				arg_string += "<button type='button' class='term' name='"+ (queries.length) + "'>"+input+"</button>" + " ";
				// Updates the HTML
				$("#queries").html(arg_string);
				// Makes the searchbear empty
				$("#query").val("");
			}
			else {
				// Makes a pop-up if term already exists
				alert ("Term Already Entered at Index: "+queries.indexOf(input));
			}
		}
		else {
			// Makes a pop-up if term is invalid
			alert ("Input Invalid");
		}
		// Not really needed, just keeps the click from doing anything unexpected.
		event.preventDefault();
	});

	//  Remove a term from the query when the term button is clicked
	$("#queries").on("click", "button.term" ,function (event) {
		// Gets the index of the clicked term
		var index = $(this).attr("name") -1;
		// If there's only one term left before removing, or if reset was pressed, wipe the whole thing and start over.
		if (queries.length == 1 || index == -1) {
			queries = [];
			arg_string = "No Terms in the Query.";
		// If there's more than one term left, just remove that term and update the array of terms & HTML
		} else {
			// Sets the term to -1
			queries[index] = -1;
			// Resets the HTML
			arg_string = starting_arg_string;

			// For each term in the array, if term != -1, transfer it to the next open spot in temp, otherwise leave it out
			// Also if it's still in the array, add a button for it in HTML
			var temp = [];
			for(var i = 0; i < queries.length; i++) {
				if (queries[i] != -1) {
					temp[temp.length] = queries[i];
					arg_string += "<button type='button' class='term' name='"+ temp.length + "'>"+queries[i]+"</button>" + " ";
				}
			}
			// Replace the old array with the new one
			queries = temp;
		}
		// Update the HTML
		$("#queries").html(arg_string);

		// Not really needed, just keeps the click from doing anything unexpected.
		event.preventDefault();
	});

	$("#search_button").click(function (event) {
		if (queries.length > 0) {
			alert('Would search on '+queries.length+' queries.');
			//$('form[name="searchbear"').submit(queries, event);
		} else {
			alert("Empty Search is Invalid");
		}
		event.preventDefault();
	});
});