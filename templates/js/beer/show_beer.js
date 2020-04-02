$(document).ready(function(){

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showBeer(){
        var beer = $.ajax({
            dataType: 'json',
            url: '/beer/get_beer',
            type: 'POST',
            // data: JSON.stringify(data),
            success: function(data) {
                console.log(data)
                for (let b of data.beer) {
                    $('#beer_container').append(`
                        <div class="col-xs-12 col-md-4">
                            <img src="${b.avatar}" alt="" class="img-responsive"  width="350" height="480">
                            <h3 class="text-center">${b.name}</h3>
                                <div class="row">
                                    <div class="col-md-4">
                                                <h4>Крепость</h4><p>${b.fortress}</p>
                                    </div>
                                    <div class="col-md-4">
                                                <h4>Плотность</h4><p>${b.gravity}</p>
                                    </div>
                                    <div class="col-md-4">
                                                <h4>IBU</h4><p>${b.ibu}</p>
                                    </div>
                                </div>
                            <h4>Описание</h4><p>${b.review}</p>
                            <h4>Производитель</h4><p>${b.manufacturer}</p>
                            <h4>Оценка</h4><p>${b.rate}</p>
                            <h4>Примечание</h4><p>${b.others}d</p>
                        </div>`);
                }
            }
        })
    }

    showBeer()

})