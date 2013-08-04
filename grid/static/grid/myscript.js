$.fn.editable.defaults.mode = 'inline';

$(document).ready(function() {
    $('a[data-toggle="tab"]').on('shown', function (e) {
      var activeTab = $(this).parent().attr('id');
      $.cookie("grid", activeTab);
    })

    $('.edit').editable({
      showbuttons: 'bottom',
      number: 3,
      savenochange:true,
      highlight:true,
      success: $.proxy(updatedReviewResponse, $(this)),
    });
    
    $('#myTab a').not('.addtab').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
    });

    if ($.cookie("grid") != null) {
      var tab_id = "#" + $.cookie("grid") + ' a';
      console.log('test')
      $(tab_id).tab('show');
    }

   $() 
   $('.search').editable({
      showbuttons: 'bottom',
      number: 2,
    });
    
    $('a.showmap').on('click', function(e) {e.preventDefault(); return true;});

    $('.remove-user').click(function(){
        var current_grid = $(this).closest('table').attr('id');
        var user_id = $(this).attr('id');
        var request = $.ajax({
          type: "POST",
          url: "/grid/remove_user/",
          dataType:'json',
          data: JSON.stringify({'removed_id':user_id, 'group':current_grid}),
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

function updatedReviewResponse(response, newValue) {
  var obj = JSON.parse(response); // dict key is new_review
  console.log(response.new_review);
}

function renameGridResponse(response, newValue) {
  var obj = JSON.parse(response); // dict key is new_review
  console.log(response.new_review);
}

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

  return '<img src="' + src + '" />';

}

$(document).ready(function() {

	$('.showmap').click(function() {
    $(this).popover('toggle');
});
});
