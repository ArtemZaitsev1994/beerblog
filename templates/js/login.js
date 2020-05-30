$(document).ready(function(){

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(mess){
        $('#error').html('');
        $('#success').html(mess);
        $('#upload_gif').show();

    }


    login = function(e){
        e.preventDefault()
        errors = ''

        if ($('#login').val().length < 1){
            errors += 'Введи логин.<br>'
        }
        if ($('#password').val().length < 1){
            errors += 'Введи пароль.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        data = {
            'login': $('#login').val(),
            'password': $('#password').val()
        }

        $.ajax({
            dataType: 'json',
            url: '/login',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                if (data.success) {
                    window.location.replace('/');
                } else {
                    showError(data.message)
                }
            }
        });


    }

    $('#submit').click(login)
    $('.credantials').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            login(e)
        }
    })

    $('#clear_photo_input').on('click', function(e){
        $('#photo').val('')
    })


})