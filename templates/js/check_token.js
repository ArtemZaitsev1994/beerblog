local_token = localStorage.getItem('Authorization')
cookie_token = $.cookie('Authorization')

url = new URL(window.location.href)
section = url.pathname.split('/')[1]

if (cookie_token === undefined && local_token === null){
    // Если у нас нет токена нигде, просим сервер ссылку на авторизацию
    $.ajax({
        dataType: 'json',
        url: '/get_auth_link',
        type: 'POST',
        data: JSON.stringify({'section': section}),
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
    $.removeCookie('Authorization', { path: '/' })
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
            request.setRequestHeader("section", section);
        },
        success: function(data){
            console.log(data)
            if (data.success){

            } else {
                window.location.replace(data.auth_link);
            }
        }
    })
}