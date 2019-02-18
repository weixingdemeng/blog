function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$.ajax({
    url:'/user/auth2/',
    type:'GET',
    dataType:'json',
    success:function(data){
        console.log(data)
        if (data.code == '200'){
            $('#real-name').val(data.username)
            $('#real-name').attr('disabled', 'disabled')
            $('#id-card').val(data.id_card)
            $('#id-card').attr('disabled', 'disabled')
            $('#auth_save').hide()
        }

    },
    error:function(data){
        alert('请求失败')
    }
})
$(document).ready(function(){


    $('#form-auth').submit(function(e){
        e.preventDefault();
        real_name = $('#real-name').val()
        id_card = $('#id-card').val()
        $.ajax({
            url:'/user/my_auth/',
            dataType:'json',
            data:{'real_name':real_name, 'id_card':id_card},
            type:'GET',
            success:function(data){
                console.log(data)
                $('.error-msg').html(data.msg)
                $('.error-msg').show()
                if (data.code == '200'){
//                    $('#auth_save').hide()
                    location.href = '/user/my/'
                }
            },
            error:function(data){
                alert('请求失败')

            }
        })

    })

})

