
function logout() {
    console.log('123')
    $.get("/user/logout/", function(data){
         console.log(data)
        if (data.code == '200') {
            location.href = "/user/index/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/user/user_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            $('#order a').attr('href', '/order/orders/'+data.data.id+'/')
            $('#order').show()
            $('#order2 a').attr('href', '/order/lorders/'+data.data.id+'/')
            $('#order2').show()
            $('#user-name').html(data.data.name)
            $('#user-name').show()
            $('#user-mobile').html(data.data.phone)
            $('#user-mobile').show()
            $('#user-avatar').attr('src', '/static/media/'+ data.data.avatar + '/')
            $('#user-avatar').show()

        }
    })

})