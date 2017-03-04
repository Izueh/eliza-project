$(document).ready(function(){
    $('#eliza-form').on('submit', function(e){
        var human_msg = $('#eliza-prompt').val();

        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/DOCTOR',
            contentType: 'application/json',
            data: JSON.stringify({ "human": human_msg}),
            success : function(data){
                $('#chat-area').append('<p>' + 'You: ' + human_msg + '</p>');
                $('#chat-area').append('<p>' + 'Eliza: ' + data.eliza + '</p>');
                $('#eliza-prompt').val('');
            }
        });
    });
});
