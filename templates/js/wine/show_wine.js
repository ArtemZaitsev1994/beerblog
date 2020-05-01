console.log(`В моей душе лежит сокровище,
И ключ поручен только мне!
Ты право, пьяное чудовище!
Я знаю: истина в вине.`)


$(document).ready(function(){

    var page = 0

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showItems(e){
        e.preventDefault()

        if (this.id == 'next_link') {
            page += 1
        } else {
            page -= 1
        }

        sorting = $('#sort').val()
        data = {
            'page': page,
            'sorting': sorting
        }

        $.ajax({
            dataType: 'json',
            url: `/wine/get_wine`,
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data) {
                $('#alcohol_container').empty()
                count = 1
                row = []
                for (i=0;i<3;i++) {
                    elems = data.wine.splice(0,3)
                    for (e of elems) {
                        row.push(`
                            <div class="col-xs-12 col-md-4">
                                <img src="${e.avatar}" alt="" class="img-responsive"  width="350" height="480">
                                <h3 class="text-center">${e.name}</h3>
                                    <div class="row">
                                        <div class="col-md-4">
                                                    <h4>Крепость</h4><p>${e.alcohol}</p>
                                        </div>
                                        <div class="col-md-4">
                                                    <h4>Вид</h4><p>${e.style}</p>
                                        </div>
                                        <div class="col-md-4">
                                                    <h4>Сахар</h4><p>${e.sugar}</p>
                                        </div>
                                    </div>
                                <h4>Описание</h4><p>${e.review}</p>
                                <h4>Производитель</h4><p>${e.manufacturer}</p>
                                <h4>Оценка</h4><p>${e.rate}</p>
                                <h4>Примечание</h4><p>${e.others}d</p>
                            </div>
                        `)
                    }
                    
                    $('#alcohol_container').append(`
                        <div class="row">
                            ${row.join('')}
                        </div>`);

                    row = []
                }

                pag = data.pagination
                if (pag.page <= 1) {
                    $('#prev_link').addClass('disabled')
                } else {
                    $('#prev_link').removeClass('disabled')
                }
                if (pag.has_next) {
                    $('#next_link').removeClass('disabled')
                } else {
                    $('#next_link').addClass('disabled')
                }
            }
        })
    }

    $('.get_item_btn').on('click', showItems)
    $('#next_link').trigger('click')

    $('#sort').on('change', showItems)
})