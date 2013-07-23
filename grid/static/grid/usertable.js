$(document).ready(function() {
	$('#newfriendsearch').on('click', function(e) {e.preventDefault(); return true;});
	
	$('#myModal').show(0, onModalShow);
	console.log($('#myModal').find('form'));
	$('#myModal').find('form').submit(runSearch);
	$('#addfriend').click(function(){
		

        var table = document.getElementById('tbody');

		
		var request = $.ajax({
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
				cell1.innerHTML = "No users left to add";
			}
			else {
			for (var i = 0; i < msg.length; i++) {
 
	            var rowCount = table.rows.length;
	            var row = table.insertRow(rowCount);
	            row.setAttribute('id', msg[i].id)
	   
	            var cell1 = row.insertCell(0);
	            var cell2 = row.insertCell(1);
	            var cell3 = row.insertCell(2);
	            var cell4 = row.insertCell(3);
	            console.log(msg[i].username);
	            cell4.innerHTML = msg[i].username;
	            $(row).on('click', msg[i].id, addNewFriend);
        }}
			$('#myModal').modal();
	});
		 
		request.fail(function(jqXHR, textStatus) {
		  alert( "Request failed: " + textStatus );
		});
	});


});

function onModalShow(){
	$('#submit-button3').on('click', runSearch);
	console.log('modal will show');
}


function runSearch(){
	console.log('clicked');

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
	        var cell3 = row.insertCell(2);
	        var cell4 = row.insertCell(3);
	        console.log(msg[i].username);
	        cell4.innerHTML = msg[i].username;
            $(row).on('click', msg[i].id, addNewFriend);

			}
		}
	})
}

function addNewFriend(id) {
	console.log(id.data);
	var newrequest = $.ajax({
			type: "POST",
			url: "/grid/add_friend/",
			dataType:'json',
			data:JSON.stringify({'id':id.data}),
		}).done(function(msg) {
		console.log('here');
		$('#myModal').modal('hide');
		location.reload();
});
}
