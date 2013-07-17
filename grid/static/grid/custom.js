$(document).ready(function() {
	$('.edit').editable('http://127.0.0.1:8000/grid/update/', {
		name: $(this).attr('name'),
	});
	console.log("right here");
});