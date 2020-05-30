$('#logout').on('click', function(e){
    e.preventDefault()
    $.removeCookie('Authorization', { path: '/' })
    window.location.replace('/');
})