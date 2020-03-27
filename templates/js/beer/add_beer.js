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
            errors += 'Крепость должна быть числом'
        }
        if (isNaN(parseInt($('#gravity').val(), 10))){
            errors += 'Плотность должна быть числом'
        }
        if (isNaN(parseInt($('#rate').val(), 10))){
            errors += 'Плотность должна быть числом'
        }

        if (errors){
            showError(errors)
            return
        }

        data = {
            'name': $('#name').val(),
            'manufacturer': $('#manufacturer').val(),
            'fortress': $('#fortress').val(),
            'gravity': $('#gravity').val(),
            'rate': $('#rate').val(),
            'review': $('#review').val(),
            'others': $('#others').val(),
        }

        $.ajax({
            dataType: 'json',
            url: '/add_beer',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data) {
                console.log(data)
                showSucces()
            }
        });


    }

    $('#submit').click(send_question)
    $('input').click(send_question)
    $('textarea').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            send_question()
        }
    })

})