$('.inputWrapper input').focus(function () {
    $(this).addClass('focussed');
});

$('.inputWrapper input').blur(function () {
    if ($(this).val().length == 0) {
        $(this).removeClass('focussed');
    }
})

$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'recommend',
        success: function () {
            console.log('success');
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});
