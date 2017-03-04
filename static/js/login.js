$(document).ready(function(){
    $('#login-form').on('submit', function(e){
        username = $('#name-field').val();
        password = $('#pass-field').val();

        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/login/',
            contentType: 'application/json',
            data: JSON.stringify({ "username":username, "password": password}),
            success : function(data){
                if(data.error){
                    // display the error message in the login-error div
                    $('#login-error').text(data.error);
                }else{
                    // redirect to home page
                    window.location.href = '/';
                }
            }
        });
    });
});
