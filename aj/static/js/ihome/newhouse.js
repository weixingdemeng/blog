function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.ajax({
        url: '/home/my_newhouse/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            html_str = ''
            for (var i=0; i<data.facilities.length; i++){
                html_str += '<li><div class="checkbox"><label><input type="checkbox" name="facility" value="'+ data.facilities[i].id +'">'+ data.facilities[i].name +'</label></div></li>'
            }
            $('.house-content ul').html(html_str)
            $('.house-content').show()





            area_list = ''
            for (var i=0; i<data.areas.length; i++){
                area_list += '<option value="' + data.areas[i].id +'">'+ data.areas[i].name +'</option>'
            }
            $('#area-id').html(area_list)
        },
        error:function(data){
            alert('请求失败')
        }
    })
     $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/home/sub_newhouse/',
            dataType:'json',
            type: 'GET',
            success:function(data){
                if (data.code != '200'){
                    $('#newhouse-error-msg').html(data.msg)
                $('#newhouse-error-msg').show()
                }
                if (data.code == '200'){
                    $('#form-house-image').css({display: 'block'})
                    $('#form-house-info').css({display: 'none'})

//                    $('#form-house-info').hide()
                }

            },
            error:function(data){
                alert('请求失败')
            }

        })
    })
    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/home/patch_image/',
            dataType:'json',
            type: 'PATCH',
            success:function(data){
                console.log(data)
                $('#f-image').attr('src', '/static/media/'+ data.image +'/')
            },
            error:function(data){
                alert('请求失败')
            }

        })
    })

})


