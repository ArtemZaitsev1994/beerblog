$(document).ready(function(){

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
            url: '/beer/add_beer',
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