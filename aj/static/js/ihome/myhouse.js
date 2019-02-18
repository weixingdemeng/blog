$(document).ready(function(){
    $(".auth-warn").show();

})
$.ajax({
        url:'/home/my_home/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            if (data.code == '200'){
                $('.house-title h3').html('真实姓名：' + data.username)
//            $('.house-title').show()
            $('.house-content a').html('身份证号码：' + data.id_card)

            house_text = ''
            new_house =  '<li><div class="new-house"><a href="/home/newhouse/">发布新房源</a></div></li><div class="new-house"><a>我的房源</a></div>'

            for (var i=0; i<data.my_house.length; i++){

                house_text += '<li><a href="/home/detail/'+ data.my_house[i].id +'/"><div class="house-title"><h3>房屋ID:' + data.my_house[i].id + '</h3></div><div class="house-content"><img src="/static/media/'+ data.my_house[i].images[0].split("\\")[7] +'"><div class="house-text">'+'<ul><li>位于：'+data.my_house[i].address+'</li><li>价格：￥'+data.my_house[i].price+'/晚</li><li>发布时间：'+data.my_house[i].create_time+'</li></ul>'+'</ul></div> </div></a></li>'
            }
            house_text += '<div class="new-house"><a>其他房源</a></div>'
            for (var i=0; i<data.other_house.length; i++){
                house_text += '<li><a href="/home/detail/'+ data.other_house[i].id +'/"><div class="house-title"><h3>房屋ID:' + data.other_house[i].id + '</h3></div><div class="house-content"><img src="/static/media/'+ data.other_house[i].images[0].split("\\")[7] +'"><div class="house-text">'+'<ul><li>位于：'+data.other_house[i].area+'</li><li>价格：￥'+data.other_house[i].price+'/晚</li><li>发布时间：'+data.other_house[i].create_time+'</li></ul>'+'</ul></div> </div></a></li>'
            }
            $('#houses-list ').html(new_house + house_text)
                $('#houses-list').show()
            }
//            if (data.code == '201'){
//                $('#to_auth').attr('color', 'red')
//            }

        },
        error:function(data){
            alert('请求失败')
        }
    })