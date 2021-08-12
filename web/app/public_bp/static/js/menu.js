$(document).ready(function() {

$('html').removeClass('no-js');

$('.dmenu-click a').on('click', function () {

  var el = $(this);

  el.parent().toggleClass('dmenu-active');

  el.parent().siblings('.dmenu-click.dmenu-active').removeClass('dmenu-active');
});

});