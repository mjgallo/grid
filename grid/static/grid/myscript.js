$.fn.editable.defaults.mode = 'inline';

$(document).ready(function() {
    $('.edit').editable({
    	type:'textarea',
    	showbuttons: 'bottom',
    });

    $('a.showmap').on('click', function(e) {e.preventDefault(); return true;});
});

var page = '<img src="https://si0.twimg.com/profile_images/1370359848/KatrinaKBowden_bigger.jpg"/>'
$(document).ready(function() {
	$('.showmap').popover( {
		placement:'top',
		trigger: 'manual',
		content: function(){
			return getMap({center:$(this).attr('data-location'),
							markers:$(this).attr('data-location')
						})
		},
		html: true,
		animation: true,
		});
});

var getMap = function(opts) {
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
  console.log(src);
  return '<img src="' + src + '" />';
}
$(document).ready(function() {
	$('.showmap').click(function() {
		$(this).popover('toggle');
	});
});