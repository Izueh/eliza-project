$(document).ready(function(){
    $('#register-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/adduser',
            contentType: 'application/json',
            data: JSON.stringify({ "username": "manan", "password": "pa$$word" , "email": "manan@abc.com"})
        });
    });
});