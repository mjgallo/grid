var map;
var infoWindow;
var service;
var london;


function initialize() {
	london= new google.maps.LatLng(51.519092, -0.098190);
  
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: london,
    zoom: 11,
    styles: [
      {
        stylers: [
          { visibility: 'simplified' }
        ]
      },
      {
        elementType: 'labels',
        stylers: [
          { visibility: 'on' }
        ]
      }
    ]
  });
  var attribution = document.getElementById('attributions');
  infoWindow = new google.maps.InfoWindow();
  service = new google.maps.places.PlacesService(map);

  //google.maps.event.addListenerOnce(map, 'bounds_changed', performSearch);
}



function callback(results, status) {
  if (status != google.maps.places.PlacesServiceStatus.OK) {
    alert(status);
    return;
  }
  else {
  	$("#searchresults").empty();
  }
  for (var i = 0, result; result = results[i]; i++) {
    createMarker(result, i);
    service.getDetails({reference:result.reference}, detailsCallback(i));
  }
}

function detailsCallback(result_num) {
	return function(place, status) {
	var number;
	var street;
	var postcode; 
  var address;

  	for (var i = 0; i < place.address_components.length; i++){
		var attr = place.address_components[i];
		if (attr.types[0] == 'street_number') 
		  number = attr.short_name;
		if (attr.types[0] == 'route') 
		  street = attr.short_name;
		if (attr.types[0] == 'postal_code') 
		  postcode = attr.short_name;
	}	
  var arrLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];

  if(typeof number !== "undefined" && typeof street !== "undefined") {
    address = number + ' ' + street;
  }
  else if (typeof street !== "undefined"){
    address = street;
  }  
  else{
    address = ' ';
  }

  var phone = place.formatted_phone_number;
  var open = place.opening_hours;
  var name = place.name;
  var url = place.website;

  if(typeof postcode !== "undefined") {
    // obj is a valid variable, do something here.
}

  var button_text = '<p align="left" style="display:inline-block">' + arrLetter[result_num] + ' </p><p align="right" style="display:inline-block"><b>' + name + '</b><br>' + address + '<br>' + postcode + '</p>';	 
  var button = document.createElement("button");
  button.setAttribute('class', 'btn btn-xlarge');
  button.setAttribute('type', 'button');
  button.setAttribute('value', arrLetter[result_num]);
  //button.setAttribute('style', 'max-width:')
  var jbutton = $(button);


  jbutton.append(button_text);
  $("#searchresults").append(button);
  $("#searchresults").css('display', 'block');
  jbutton.click(function(){
  	$.ajax({
  	data: JSON.stringify({'name': name, 'address': address, 'phone': phone, 'website':url, 'postcode':postcode}),
  	type: "POST",
  	url: "/grid/add_restaurant/",
  	success: function(){
  		$("#searchresults").empty();
  		$("#map-canvas").css('display', 'none');
  		location.reload();
  	},
  	dataType:'json',
  });
});
}
}

function createMarker(place, index) {
  var arrLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
  var iconUrl = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + arrLetter[index] + '|FF0000|000000';
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location,
    icon: iconUrl
  });

  google.maps.event.addListener(marker, 'click', function() {
    service.getDetails(place, function(result, status) {
      if (status != google.maps.places.PlacesServiceStatus.OK) {
        alert(status);
        return;
      }
      infoWindow.setContent(result.name);
      infoWindow.open(map, marker);
    });
  });
}

//google.maps.event.addDomListener(window, 'load', initialize);

$(document).ready(function() {
  $('#newrestsearch').on('submit', function(e) {e.preventDefault(); return true;});
	$('#newrestsearch').submit(function(){

		initialize();

		var search = '"' + $('#new-rest-search-params').val()+ '"';
		var request = {
			location:london,
			radius:'10000',
		    name: search,
		};
		service.radarSearch(request, callback);
		$("#map-canvas").css('display', 'block');
	});

});



