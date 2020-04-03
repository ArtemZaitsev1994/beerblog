$(document).ready(function(){

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(){
        $('#error').html('');
        $('#success').html('Вопрос успешно отправлен.');
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
        data.append('photo', $('#photo')[0].files[0])
        data.append('gravity', $('#gravity').val())
        // data1 = {
        //     'name': $('#name').val(),
        //     'manufacturer': $('#manufacturer').val(),
        //     'fortress': $('#fortress').val(),
        //     'gravity': $('#gravity').val(),
        //     'rate': $('#rate').val(),
        //     'review': $('#review').val(),
        //     'others': $('#others').val(),
        //     'photo': $('#photo')[0].files[0],
        // }

        console.log(data)
        $.ajax({
            dataType: 'json',
            url: '/beer/add_beer',
            type: 'POST',
            // data: JSON.stringify(data),
            data: data,
            processData: false,
            contentType: 'multipart/form-data; boundary=----WebKitFormBoundaryAfue2PxayUdscUBZ',
            success: function(data) {
                console.log(data)
                showSucces()
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