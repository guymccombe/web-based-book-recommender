$('#formSwapper').click(e => {
    e.preventDefault();
    $('body').toggleClass('moveBackgroundRight');
    $('#login').toggleClass('register');

    if($('#login').hasClass('register')) {
        $('#formTitle, #loginButton').text('Register');
        $('#registerPrompt').text('Regular reader? ');
        $('#formSwapper').text('Log in!');
        document.title = 'Register | BookClub'
    } else {
        $('#formTitle, #loginButton').text('Log in');
        $('#registerPrompt').text('New to us?')
        $('#formSwapper').text('Join now!');
        document.title = 'Log in | BookClub'
    }
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
    url = ($('#login').hasClass('register') ? '/register' : '/login');
    data = {
        'username': $('input[name=username]').val()
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json'
    });
});