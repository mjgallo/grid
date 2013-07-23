$(document).ready(function() {
	$('#newfriendsearch').on('click', function(e) {e.preventDefault(); return true;});
	$('#addfriend').click(function(){
		
        var table = document.getElementById('tbody');
		
		var request = $.ajax({
  			type: "GET",
  			url: "/grid/find_users/",
  			dataType:'json',
  		});

		request.done(function(msg) {
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
        }
			$('#myModal').modal();
	});
		 
		request.fail(function(jqXHR, textStatus) {
		  alert( "Request failed: " + textStatus );
		});
	});
		$('#newfriendsearch').submit(function(){
		console.log('clicked');

		var table = document.getElementById('tbody');
		
		var request = $.ajax({
			data: $('#new-rest-search-params').val(),
  			type: "GET",
  			url: "/grid/find_users/",
  			dataType:'json',
  		});

		request.done(function(msg) {
			for (var i = 0; i < msg.length; i++) {
 
            var rowCount = table.rows.length;
            var row = table.insertRow(rowCount);
   
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            console.log(msg[i].username);
            cell4.innerHTML = msg[i].username;
        }
	})
});
});

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
