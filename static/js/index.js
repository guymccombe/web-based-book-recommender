$(document).ready(function(){
    console.log('JQuery loaded.');
});

$('#signup').click(e => {
    e.preventDefault();
    $('body').toggleClass('moveBackgroundRight');
});

$('.inputWrapper input').focus(function() {
    $(this).addClass('focussed');
});

$('.inputWrapper input').blur(function() {
    if($(this).val().length == 0) {
        $(this).removeClass('focussed');
    }
})

$('#loginButton').click(e => {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/login',
        data: JSON.stringify($('#login').serialize()),
        contentType: 'application/json',
        dataType: 'json'
    });
});