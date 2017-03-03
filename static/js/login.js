$(document).ready(function(){
    $('#login-form').on('submit', function(e){
        username = $('#name-field').val();
        password = $('#pass-field').val();

        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/login/',
            contentType: 'application/json',
            data: JSON.stringify({ "username":username, "password": password})
        });
    });
});
