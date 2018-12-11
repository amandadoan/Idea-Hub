$(".respond-button").click(function() {
	//$("#modalDisplay").html("")
	//$("#modalDisplay").show();
});

// $("#make-post").click(function(event){
// 	event.preventDefault();
// 	$("#modalDisplay").html("<div class='modal-content'><span class='close'>&times;</span></br><form action='" +"{% url 'makePost' project.project_name %}"+"' method='post'><div class='form-group'><label for='type'>Type:</label><select class='form-control' id='type' type='text' name='type'> <option value='C'>Comment</option><option value='Q'>Question</option> {% if canUpdate == True %} <option value='U'>Update</option> {% endif %} </select></div><div class='form-group'> <label for='content'>Message:</label><textarea name='content' id='content' class='form-control' rows='3'></textarea></div><input type='submit' class='btn btn-success float-right' value='Post'></input><button class='cancel btn btn-danger float-right'>Cancel</button> {% csrf_token %} </form></div>");
// 	$("#modalDisplay").show();
// });

$(".cancel").click(function(event) {
	event.preventDefault();
	$("#modalDisplay").hide();
});

$(".close").click(function(){
	$("#modalDisplay").hide();
});

