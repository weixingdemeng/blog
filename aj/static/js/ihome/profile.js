function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

    $("#form-avatar").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/my_profile/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                console.log(data)
                if (data.code == '200'){
                    console.log(data.path)
                    $('#user-avatar').attr('src', '/static/media/'+ data.path + '/')
                }
            },
            error:function(data){
                alert('请求失败')
            }
            })
        })
    $("#form-name").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/name_profile/',
            type:'PATCH',
            dataType:'json',
            success:function(data){
                console.log(data)
                if (data.code == '3001'){
                    $('.error-msg i').html(data.msg)
                    $('.error-msg ').show()
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
        })
        })




