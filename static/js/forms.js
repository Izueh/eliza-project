$(document).ready(function(){
    $('#login-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/login/',
            contentType: 'application/json',
            data: JSON.stringify({ "username": "manan", "password": "pa$$word" })
        });
    });
});