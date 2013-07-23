$.fn.editable.defaults.mode = 'inline';

$(document).ready(function() {

    $('.edit').editable({
    	showbuttons: 'bottom',
    	number: 3,
    	savenochange:true,
    	highlight:true,
    });

   $('.search').editable({
      showbuttons: 'bottom',
      number: 2,
    });
    
    $('a.showmap').on('click', function(e) {e.preventDefault(); return true;});

    $('.remove-user').click(function(){
        var user_id = $(this).attr('id');
        var request = $.ajax({
          type: "POST",
          url: "/grid/remove_user/",
          dataType:'json',
          data: JSON.stringify({'removed_id':user_id}),
        }).done(function(msg) {
          location.reload();
        });
    });
});
var page = '<img src="https://si0.twimg.com/profile_images/1370359848/KatrinaKBowden_bigger.jpg"/>'
$(document).ready(function() {


	$('.showmap').popover( {
		placement:'top',
		trigger: 'manual',
		content: function(){
			return getMap({center:$(this).attr('data-location'),
							markers:$(this).attr('data-location')
						}, true)
		},
		html: true,
		animation: true,
	});

});

var getMap = function(opts, tag) {
  var src = "http://maps.googleapis.com/maps/api/staticmap?",
  params = $.extend({
    zoom: 14,
    size: '200x200',
    maptype: 'roadmap',
    sensor: false
  }, opts),
  query = [];

  $.each(params, function(k, v) {
query.push(k + '=' + encodeURIComponent(v));
  });

  src += query.join('&');
  if (tag){
    return '<img src="' + src + '" />';
  }
  else{
    return src;
  } 
}

$(document).ready(function() {

	$('.showmap').click(function() {
    $(this).popover('toggle');
});
});
