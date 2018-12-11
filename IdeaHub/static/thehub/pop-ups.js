$(".respond-button").click(function() {
	$("#commentModal").show();
});

$("#make-post").click(function(event){
	event.preventDefault();
	$("#postModal").show();
});

$(".cancel").click(function(event) {
	event.preventDefault();
	$("#commentModal").hide();
	$("#postModal").hide();
});

$(".close").click(function(){
	$("#commentModal").hide();
	$("#postModal").hide();
});

