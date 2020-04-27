$(document).ready(function(){
    local_token = localStorage.getItem('Authorization')
    cookie_token = $.cookie('Authorization')

    if (cookie_token === undefined && local_token === null){
        // Если у нас нет токена нигде, просим сервер ссылку на авторизацию
        $.ajax({
            dataType: 'json',
            url: '/get_auth_link',
            type: 'POST',
            data: JSON.stringify({'section': 'beer'}),
            processData: false,
            contentType: false,
            success: function(data){
                if (data.success){
                    window.location.replace(data.link);
                } else {
                    draw_error('Ошибка на стороне сервера')
                }
            }
        })
    } else if (cookie_token !== undefined){
        // если токен пришел в куках 
        // приходит, если мы залогинились только что -> валидный по определению
        localStorage.setItem('Authorization', cookie_token)
        $.removeCookie('Authorization')
    } else if (local_token !== null){
        // если токен есть у нас в локал сторедже, проверям валидный ли он до сих пор
        $.ajax({
            dataType: 'json',
            url: '/api/check_token',
            type: 'POST',
            data: JSON.stringify({'token': local_token}),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", local_token);
            },
            success: function(data){
                if (data.success){

                } else {
                    window.location.replace(data.auth_link);
                }
            }
        })
    }
    token = localStorage.getItem('Authorization')
    console.log(token)

    function checkAuth(data){
        if (!data.success && data.invalid_token){
            console.log(11111111111111111111)
            window.location.replace(data.auth_link);
        }
    }

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(mess){
        $('#error').html('');
        $('#success').html(mess);
    }


    send_review = function(){
        errors = ''

        if ($('#name').val().length < 1){
            errors += 'Добавь название.<br>'
        }
        if (isNaN(parseInt($('#fortress').val(), 10))) {
            errors += 'Крепость должна быть числом.<br>'
        }
        if (isNaN(parseInt($('#gravity').val(), 10))){
            errors += 'Плотность должна быть числом.<br>'
        }
        if (isNaN(parseInt($('#rate').val(), 10))){
            errors += 'Плотность должна быть числом.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        var data = new FormData();

        data.append('name', $('#name').val())
        data.append('manufacturer', $('#manufacturer').val())
        data.append('fortress', $('#fortress').val())
        data.append('gravity', $('#gravity').val())
        data.append('rate', $('#rate').val())
        data.append('review', $('#review').val())
        data.append('others', $('#others').val())
        data.append('photos', $('#photo')[0].files[0])
        data.append('ibu', $('#ibu').val())

        $.ajax({
            dataType: 'json',
            url: '/api/save_item',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.acknowledged) {
                    showSucces(`Пиво ${$('#name').val()} успешно добавлено.`)
                } else {
                    showSucces(data.message)
                }
            }
        });


    }

    $('#submit').click(send_review)
    $('textarea').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            send_review()
        }
    })

    $('#clear_photo_input').on('click', function(e){
        $('#photo').val('')
    })


})