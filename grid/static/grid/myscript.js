$.fn.editable.defaults.mode = 'inline';
var delete_button_clicked;
var deleteGridClone;
var activeTab;
var prevTab;

$(document).ready(function() {
    activeTab = $("#defaultGrid").html();
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

    $('#myTab').children('li').click(function(){
      prevTab = activeTab;
      activeTab = $(this).attr('id');
    });

    $('.grid-remove').click(function(){
      deleteGridClone = $('#modalGridRemove').clone();
      var div = $(this).parent('div').clone();
      $(div).children(":first").remove();
      var grid_name = div.html();
      var message = '<p>Are you sure you want to remove yourself from grid ' + grid_name + '?</p>';
      delete_button_clicked = $(this).parents('li').attr('id');
      $('#modalGridRemove').find('.modal-body').prepend(message);
      $('#modalGridRemove').modal('show').off('hidden').on("hidden", function() {
          $("#modalGridRemove").replaceWith(deleteGridClone);
        });
    });

    $("#account").popover({
        content:function() {
                  return $('#confirminvitations').html();
                },
        placement: 'bottom',
        html: true,
        title: 'Update account information'
      }).off('hidden').on("hidden", function(e) {
            $(".popover-content").css("text-align", "start");
    });


    if ($.cookie("grid") != null) {
      var tab_id = "#" + $.cookie("grid") + ' a';
      $(tab_id).tab('show');
    }

   $('.search').editable({
      showbuttons: 'bottom',
      number: 2,
    });
    
    $('a.showmap').on('click', function(e) {e.preventDefault(); return true;});

    $('.remove-restaurant').click(function(){
        var current_grid = $(this).closest('table').attr('id');
        var restaurant_id = $(this).attr('id');
        var request = $.ajax({
          type: "POST",
          url: "/grid/remove_restaurant/",
          dataType:'json',
          data: JSON.stringify({'removed_id':restaurant_id, 'group':current_grid}),
        }).done(function(msg) {
          location.reload();
        });
    });
});


$(document).on('click', '#account_update', function(e){
  e.preventDefault();
  return true;});

$(document).on('click', '#confirmDeleteButton', function(){
    var body = $(this).parent();
    var request = $.ajax({
      type: "POST",
      url: "/grid/remove_grid/",
      dataType:'json',
      data: JSON.stringify({'grid':delete_button_clicked}),
    }).done(function(msg) {
      if(msg['success']){
        body.empty();
        body.css('text-align', 'center');
        body.prepend('<img width="30%" height="30%" name="img01" src="/static/grid/check_mark_green.png">');
        body.append('<br><p>You have successfully removed yourself from the grid.</p>');
        var tab_id = '#'+delete_button_clicked;
        var removedTab = $('#myTab').find(tab_id);
        var tabWasActive = ($(removedTab).attr('id') === prevTab) ? true : false;
        var removedDivID = '#grid'+delete_button_clicked;
        var removedDiv = $(document).find(removedDivID);
        removedTab.remove();
        removedDiv.remove();
        if(tabWasActive){
          $('#myTab').children(':first').attr('class', 'active');
          $('.tab-content').children(':first').attr('class', 'tab-pane active');
        }
        else{
          var tab_id = '#'+prevTab;
          $('#myTab').children(tab_id).attr('class', 'active');
          var div_id = '#grid'+prevTab;
          $(div_id).attr('class', 'tab-pane active');
        }
      }
      else{
        body.empty();
        body.css('text-align', 'center');
        body.append('<br><p>Sorry, you cannot remove yourself from your default grid.</p>');
      }
    });
})

$(document).on('click', '#account_update', function(){
        var request = $.ajax({
          type: "POST",
          url: "/grid/update_account/",
          dataType:'json',
          data: $("#account_form").serialize(),
        }).done(function(msg) {
          $(".popover-content").children("form").remove();
          $(".popover-content").css("text-align", "center");
          $(".popover-content").prepend('<img width="60%" height="60%" name="img01" src="/static/grid/check_mark_green.png">');
          var confirmation_text = '<p>Name now ' + msg['firstname'] + ' ' + msg['lastname'] + '</p>';
          $(".popover-content").prepend(confirmation_text);
          var firstname = $("#confirminvitations").find("#fn");
          var lastname = $("#confirminvitations").find("#ln");
          $(firstname).attr('placeholder', msg['firstname']);
          $(lastname).attr('placeholder', msg['lastname']);          
        });

});

$("#account").off('hidden').on("hidden", function(e) {
    $(".popover-content").css("text-align", "start");
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
}

function renameGridResponse(response, newValue) {
  var obj = JSON.parse(response); // dict key is new_review
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
