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
            url: `/bar/get_bar`,
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data) {
                console.log(data)
                $('#alcohol_container').empty()
                count = 1
                row = []
                for (i=0;i<3;i++) {
                    elems = data.bar.splice(0,3)
                    for (e of elems) {
                        row.push(`
                            <div class="col-xs-12 col-md-4">
                                ${e}
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