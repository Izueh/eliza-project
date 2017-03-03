$(document).ready(function(e){
    $('#login-form').on('submit', function(){
        $.ajax({
            method: 'POST',
            url: '/login/',
            contentType: 'application/json',
            data: { username: "manan", password: "pa$$word" },
            dataType: "json",
            success: function(response){
                console.log(response);
            },
            failure: function(errMsg){
                console.log(errMsg)
            }
        });
    });
})
