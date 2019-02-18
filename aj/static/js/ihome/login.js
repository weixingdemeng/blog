function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        $.ajax({
            url:'/user/my_login/',
            type:'GET',
            dataType:'json',
            data:{'mobile':mobile, 'password': passwd},
            success:function(data){
                console.log(data)
                if (data.code == '2002'){
                    $("#mobile-err span").html(data.msg)
                    $('#mobile-err').show()

                }
                if (data.code == '2003'){

                    $("#password-err span").html(data.msg)
                    $('#password-err').show()
                }
                if (data.code == '200'){
                    location.href = '/user/my/'
                }

            },
            error:function(data){
                alert('失败')
            }
        })
    });
})