var current_grid;

$(document).on('click', '#addfriend', function(){
	$('#newfriendsearch').on('click', function(e) {e.preventDefault(); return true;});
	$('#newfriendinvitation').on('click', function(e) {e.preventDefault(); return true;});
	
	$('#myModal').show(0, onModalShow); /* provides a signal to add submit listener to search form */

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
	$('#submit-button5').on('click', inviteFriend);
}

function inviteFriend(){
	var request = $.ajax({
			type: "POST",
			url: "/invite/send/",
			dataType:'json',
			data: JSON.stringify({'grid': current_grid.toString(), 'email':$('#invitationemail').val()}),
	}).done(function(msg) {
		$('#myModal').modal('hide');
	});
}

function runSearch(){
	console.log('search run');
	var table = document.getElementById('tbody');
	
	var request = $.ajax({
			data: JSON.stringify({'search-string':$('#friendsearchparams').val(), 'group':current_grid.toString()}),
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

$(document).on('click', '#joingrid', function(){

	$('#newgridjoin').on('click', function(e) {e.preventDefault(); return true;});
	
	$('#myModalJoin').show(0, onJoinModalShow);
	$('#myModalJoin').find('form').submit(runGridSearch);

	console.log('NEWGRID JOIN ACTIVATING');

        var table = document.getElementById('tbodyjoin');

		var request = $.ajax({
  			type: "GET",
  			url: "/grid/find_grid/",
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
				cell1.setAttribute('colspan', 5);
				cell1.innerHTML = "No grids left to add";
			}
			else {
			for (var i = 0; i < msg.length; i++) {
 
	            var rowCount = table.rows.length;
	            var row = table.insertRow(rowCount);
	            row.setAttribute('id', msg[i].id)
	   
	            var cell1 = row.insertCell(0);
	            var cell2 = row.insertCell(1);
	            cell2.innerHTML = msg[i].founder;
	            var cell3 = row.insertCell(2);
	            cell3.innerHTML = msg[i].name;
	            var cell4 = row.insertCell(3);
	            var cell5 = row.insertCell(4);
	            cell5.innerHTML = msg[i].count;
	            $(row).on('click', msg[i].id, joinNewGrid);
        }}
			$('#myModalJoin').modal();
	});
		 
		request.fail(function(jqXHR, textStatus) {
		  alert( "Super failed: " + textStatus );
		});
});

function joinNewGrid(id) {
	var newrequest = $.ajax({
			type: "POST",
			url: "/grid/request_grid/",
			dataType:'json',
			data:JSON.stringify({'id':id.data}),
		}).done(function(msg) {
			console.log('about to hide');
		$('#myModalJoin').modal('hide');
});
}

function onJoinModalShow(){
	$('#submit-button4').on('click', runGridSearch);
}

function runGridSearch(){
		console.log('search run');
        var table = document.getElementById('tbodyjoin');
	
	var request = $.ajax({
			data: JSON.stringify({'search-string':$('#gridjoinparams').val()}),
			type: "GET",
			url: "/grid/find_grid/",
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
				cell1.setAttribute('colspan', 5);
				cell1.innerHTML = "No grids left to add";
			}
			else {
			for (var i = 0; i < msg.length; i++) {
 
	            var rowCount = table.rows.length;
	            var row = table.insertRow(rowCount);
	            row.setAttribute('id', msg[i].id)
	   
	            var cell1 = row.insertCell(0);
	            var cell2 = row.insertCell(1);
	            cell2.innerHTML = msg[i].founder;
	            var cell3 = row.insertCell(2);
	            cell3.innerHTML = msg[i].name;
	            var cell4 = row.insertCell(3);
	            var cell5 = row.insertCell(4);
	            cell5.innerHTML = msg[i].count;
	            $(row).on('click', msg[i].id, joinNewGrid);
        }}
    });

}

$(document).on('click', '.approvemember', function() {
	var current_grid = $(this).closest('.overarchingdiv').attr('id');
	console.log(current_grid);
	var approved_user = $(this).attr('id');
	console.log(approved_user);
	var newrequest = $.ajax({
		type: "POST",
		url: "/grid/approve_request/",
		dataType:'json',
		data:JSON.stringify({'approved_id':approved_user.toString(), 'grid':current_grid.toString()}),
	}).done(function(msg) {
	location.reload();
	});
});