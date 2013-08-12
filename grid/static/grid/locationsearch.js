var map;
var infoWindow;
var service;
var london;
var current_grid;
var details_array = new Array();
var index_array = new Array();

function initialize() {
	london= new google.maps.LatLng(51.519092, -0.098190);
  
  var map_id = 'map-canvas' + current_grid.toString();
  console.log(map_id);
  map = new google.maps.Map(document.getElementById(map_id), {
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
    var searchresults_id = "#searchresults" + current_grid.toString();
    $(searchresults_id).empty();
    $(searchresults_id).append("<p>Nothing found. Search again or add manually.");
    $(searchresults_id).css('display', 'block');

    return;
  }
  else {
    var searchresults_id = "#searchresults" + current_grid.toString();
  	$(searchresults_id).empty();
  }
  for (var i = 0, result; i<15; i++) {
    try{
      createMarker(results[i], i);
      service.getDetails({reference:results[i].reference}, detailsCallback(i));
    }
    catch(TypeError){
      console.log('TypeError - detailsCallback');
    }
  }
  console.log('yeah I inline-block');
  
  setTimeout(function(){
  for (var i = 0; i < index_array.length; i++) {
    var index = index_array.indexOf(i);
    $(searchresults_id).append(details_array[index]);
    //Do something
  }
    $('.editableform-loading').css('display', 'none');

    $(searchresults_id).css('display', 'block');
    $("#newrestmanualadd").css('display', 'block');
    $('#submit-button-manual').off('click').on('click', manualAdd);

  }, 1000);
}

function manualAdd(){
    var rest_name_manual_id = '#new-rest-manual' + current_grid.toString();
    var request = $.ajax({
      type: "POST",
      url: "/grid/rest_manual_add/",
      dataType:'json',
      data: JSON.stringify({'grid': current_grid.toString(), 'name':$(rest_name_manual_id).val()}),
  }).done(function(msg) {
      $(rest_name_manual_id).empty();
      $("#map-canvas").css('display', 'none');
      location.reload();
})
}

function detailsCallback(result_num) {
	return function(place, status) {
	var use_detail_result = true;
  try{
    var name = place.name;
  }
  catch(TypeError){
    use_detail_result = false;
    console.log(TypeError)
  }

if(use_detail_result){
  var number;
	var street;
	var postcode; 
  var address;
  try {
  	for (var i = 0; i < place.address_components.length; i++){
		var attr = place.address_components[i];
		if (attr.types[0] == 'street_number') 
		  number = attr.short_name;
		if (attr.types[0] == 'route') 
		  street = attr.short_name;
		if (attr.types[0] == 'postal_code') 
		  postcode = attr.short_name;
	 }
  }	
  catch(TypeError){
    console.log('TypeError')
  }
  var arrLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N','O','P','Q','R'];

  if(typeof number !== "undefined" && typeof street !== "undefined") {
    address = number + ' ' + street;
  }
  else if (typeof street !== "undefined"){
    address = street;
  }  
  else{
    address = ' ';
  }

  try{
      var phone = place.formatted_phone_number;
  }
  catch(TypeError){
    console.log(TypeError)
  }
  try{
    var open = place.opening_hours;
  }
  catch(TypeError){
    console.log(TypeError)
  }
  try{
    var url = place.website;
  }
  catch(TypeError){
    console.log(TypeError)
  }
  try{
    var price = place.price_level;
  }
  catch(TypeError){
    console.log(TypeError)
  }

  console.log('WWWWTTTTFFFF');
  var button_text = '<p align="left" style="display:inline-block;vertical-align:top;padding-right:6px;position:absolute;left:8px;top:8px">(' + arrLetter[result_num] + ') </p><p align="right" style="display:inline-block;position:absolute;right:8px;top:8px"><b>' + name + '</b><br>' + address + '<br>' + postcode + '</p>';	 
  var button = document.createElement("button");
  button.setAttribute('type', 'button');
  button.setAttribute('value', arrLetter[result_num]);
  //button.setAttribute('style', 'max-width:')
  var jbutton = $(button);

  var searchresults_id = "#searchresults" + current_grid.toString();

  jbutton.append(button_text);
  $(button).attr('class','btn btn-info');
  $(button).css('width','230px');
  $(button).css('height','80px');
  $(button).css('position','relative');

  var div=document.createElement("div");
  div.setAttribute('align','right');

  $(div).append(button);
  $(div).css('padding', '5');
  var table_id = $('table').attr('id');
  console.log('pushing');
  details_array.push(div);
  index_array.push(result_num);

  var data = JSON.stringify({'group': current_grid, 'name': name, 'address': address, 'phone': phone, 'website':url, 'postcode':postcode, 'price':price});
  var escapeddata = escape(data);
  jbutton.click(function(){
  	$.ajax({
  	data: escapeddata,
  	type: "POST",
  	url: "/grid/add_restaurant/",
  	success: function(){
  		$(searchresults_id).empty();
  		$("#map-canvas").css('display', 'none');
  		location.reload();
  	},
  	dataType:'json',
  });
});
}
}
}

function createMarker(place, index) {
  var arrLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N','O','P','Q'];
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

$(document).on('submit', '#newrestsearch', function(e) {e.preventDefault(); return true;});
/*	
  $('#newrestsearch').submit(function(){
    current_grid = $(this).closest('table').attr('id');
    console.log(current_grid);
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
*/

$(document).on('submit', "#newrestsearch", function() {
    current_grid = $(this).closest('table').attr('id');
    index_array = [];
    details_array = [];
    console.log(current_grid);
    initialize();
    $('.editableform-loading').css('display', 'block');
    var rest_search_params = '#new-rest-search-params' + current_grid.toString();

    var search = '"' + $(rest_search_params).val()+ '"';
    var request = {
      location:london,
      radius:'10000',
      name: search,
      types:["bar","spa","night_club","grocery_or_supermarket","restaurant","meal_delivery","meal_takeaway","cafe","food"],
    };
    service.radarSearch(request, callback);
    var map_id = '#map-canvas' + current_grid.toString();
    $(map_id).css('display', 'block');
    setTimeout(function() {
      google.maps.event.addListener(map, 'idle', function() {
      var request_bounds = {
        bounds: map.getBounds(),
        name: search,
        types: ["bar","spa","night_club","grocery_or_supermarket","restaurant","meal_delivery","meal_takeaway","cafe","food"],
      };
      index_array = [];
      details_array = [];
      $('.editableform-loading').css('display', 'block');
      service.radarSearch(request_bounds, callback);
      console.log('bounds change search');
    });
    }, 1000);
});


