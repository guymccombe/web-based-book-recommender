$('.inputWrapper input').focus(function() {
    $(this).addClass('focussed');
});

$('.inputWrapper input').blur(function() {
    if($(this).val().length == 0) {
        $(this).removeClass('focussed');
    }
})
