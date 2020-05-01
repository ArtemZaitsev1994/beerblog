$(document).ready(function(){
    token = localStorage.getItem('Authorization')

    function checkAuth(data){
        if (!data.success && data.invalid_token){
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


    send_review = function(e){
        e.preventDefault()
        errors = ''

        if ($('#name').val().length < 1){
            errors += 'Добавь название.<br>'
        }
        if (isNaN(parseInt($('#rate').val(), 10))){
            errors += 'Плотность должна быть числом.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        var data = new FormData();
        data.append('alcohol_type', 'vodka')
        data.append('name', $('#name').val())
        data.append('manufacturer', $('#manufacturer').val())
        data.append('rate', $('#rate').val())
        data.append('review', $('#review').val())
        data.append('others', $('#others').val())
        if ($('#photo')[0].files[0] !== undefined){
            data.append('photos', $('#photo')[0].files[0])
        }

        $.ajax({
            dataType: 'json',
            url: '/api/save_item',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
                request.setRequestHeader("section", section);
            },
            success: function(data) {
                checkAuth(data)
                if (data.success) {
                    showSucces(`Водка ${$('#name').val()} успешно добавлена.`)
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