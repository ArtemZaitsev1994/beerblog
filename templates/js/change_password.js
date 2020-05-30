$(document).ready(function(){

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(mess){
        $('#error').html('');
        $('#success').html(mess);

    }


    change_password = function(e){
        e.preventDefault()
        errors = ''

        if ($('#old_password').val().length < 1){
            errors += 'Введи текущий пароль.<br>'
        }
        if ($('#new_password').val().length < 1){
            errors += 'Введи новый пароль.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        data = {
            'old_password': $('#old_password').val(),
            'new_password': $('#new_password').val()
        }

        $.ajax({
            dataType: 'json',
            url: '/change_password',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                console.log(data)
                if (data.success) {
                    showSucces('Пароль сменен.');
                } else {
                    showError(data.message)
                }
            }
        });


    }

    $('#submit').click(change_password)
    $('.credantials').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            change_password(e)
        }
    })


})