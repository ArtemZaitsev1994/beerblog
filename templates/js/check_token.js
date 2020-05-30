// token = $.cookie('Authorization')

// url = new URL(window.location.href)
// section = url.pathname.split('/')[1]

// if (token === undefined){
//     // Если у нас нет токена нигде, просим сервер ссылку на авторизацию
//     $.ajax({
//         dataType: 'json',
//         url: '/get_auth_link',
//         type: 'POST',
//         data: JSON.stringify({'section': section}),
//         processData: false,
//         contentType: false,
//         success: function(data){
//             if (data.success){
//                 window.location.replace(data.link);
//             } else {
//                 draw_error('Ошибка на стороне сервера')
//             }
//         }
//     })
// } else {
//     // если токен есть у нас в локал сторедже, проверям валидный ли он до сих пор
//     $.ajax({
//         dataType: 'json',
//         url: '/api/check_token',
//         type: 'POST',
//         data: JSON.stringify({'token': token}),
//         processData: false,
//         contentType: false,
//         beforeSend: function(request) {
//             request.setRequestHeader("Authorization", token);
//             request.setRequestHeader("section", section);
//         },
//         success: function(data){
//             if (data.success){

//             } else {
//                 window.location.replace(data.auth_link);
//             }
//         }
//     })
// }