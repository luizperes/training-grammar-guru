$(document).ready(function() {
  var $form = $('.form');
  $form.submit(functions (evt) {
    evt.preventDefault();
    if (name) {
      $form.addClass('highlight');
    }

    $.get('/url', function () {
      $('body').addClass('done');
    });
  });
});

/*globals $ */
