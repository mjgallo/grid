$(document).on('click', '#addfriend', function(){
	$('#newfriendsearch').on('click', function(e) {e.preventDefault(); return true;});
	
	$('#myModal').show(0, onModalShow);
	$('#myModal').find('form').submit(runSearch);
	console.log('clicked');
		current_grid = $(this).closest('table').attr('id');
        var table = document.getElementById('tbody');

		
		var request = $.ajax({
  			type: "GET",
  			url: "/grid/find_users/",
  			dataType:'json',
  			data: JSON.stringify({'group': current_grid}),
  		});

		request.done(function(msg) {
			while(table.hasChildNodes()) {
				table.removeChild(table.firstChild);
			}
			if (msg.length === 0){
				var rowCount = table.rows.length;
				var row = table.insertRow(rowCount);
				var cell1 = row.insertCell(0);
				cell1.setAttribute('colspan', 4);
				cell1.innerHTML = "No users left to add";
			}
			else {
			for (var i = 0; i < msg.length; i++) {
 
	            var rowCount = table.rows.length;
	            var row = table.insertRow(rowCount);
	            row.setAttribute('id', msg[i].id)
	   
	            var cell1 = row.insertCell(0);
	            var cell2 = row.insertCell(1);
	            cell2.innerHTML = msg[i].first_name;
	            var cell3 = row.insertCell(2);
	            cell3.innerHTML = msg[i].last_name;
	            var cell4 = row.insertCell(3);
	            cell4.innerHTML = msg[i].username;
	            $(row).on('click', msg[i].id, addNewFriend);
        }}
			$('#myModal').modal();
	});
		 
		request.fail(function(jqXHR, textStatus) {
		  alert( "Request failed: " + textStatus );
		});
	});



function onModalShow(){
	$('#submit-button3').on('click', runSearch);
}


function runSearch(){

	var table = document.getElementById('tbody');
	
	var request = $.ajax({
			data: JSON.stringify({'search-string':$('#friendsearchparams').val()}),
			type: "GET",
			url: "/grid/find_users/",
			dataType:'json',
		});

	request.done(function(msg) {
		while(table.hasChildNodes()) {
			table.removeChild(table.firstChild);
		}
		if (msg.length === 0){
			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);
			var cell1 = row.insertCell(0);
			cell1.setAttribute('colspan', 4);
			cell1.innerHTML = "No users found";
		}
		else {

			for (var i = 0; i < msg.length; i++) {

	        var rowCount = table.rows.length;
	        var row = table.insertRow(rowCount);

            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            cell2.innerHTML = msg[i].first_name;
            var cell3 = row.insertCell(2);
            cell3.innerHTML = msg[i].last_name;
            var cell4 = row.insertCell(3);
            cell4.innerHTML = msg[i].username;
            $(row).on('click', msg[i].id, addNewFriend);

			}
		}
	})
}

function addNewFriend(id) {
	var newrequest = $.ajax({
			type: "POST",
			url: "/grid/add_friend/",
			dataType:'json',
			data:JSON.stringify({'id':id.data, 'group': current_grid}),
		}).done(function(msg) {
		$('#myModal').modal('hide');
		location.reload();
});
}

$(document).ready(function(){
	$("#creategrid").click(function(){
		$('#myModalGrid').modal('toggle');
		current_grid = $(this).closest('table').attr('id');
	});
});

$(document).on('click', '.editgrid', function() {
	$('#updategrid').on('submit', function(e) {e.preventDefault(); return true;});
	console.log('i am clicked');
	$('#myModalGridUpdate').modal('toggle');
	var current_grid = $(this).closest('div').attr('id');
	$(document).on('submit', '#updategrid', function(){
		var new_name= $('#newgridname').val();
		console.log(new_name);
		var new_description = $('#newgriddescription').val();
		var newrequest = $.ajax({
			type: "POST",
			url: "/grid/update_grid/",
			dataType:'json',
			data:escape(JSON.stringify({'name':new_name, 'description': new_description, 'id': current_grid.toString()})),
		}).done(function(msg) {
		$('#myModalGridUpdate').modal('hide');
		location.reload();
	})
});
});

$(document).on('click', '.approvegrid', function() {
	var approved_grid = $(this).attr('id');
			var newrequest = $.ajax({
			type: "POST",
			url: "/grid/approve_grid/",
			dataType:'json',
			data:JSON.stringify({'approved_id':approved_grid.toString()}),
		}).done(function(msg) {
		location.reload();
});
	});
