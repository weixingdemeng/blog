function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var test = window.location.pathname;
    var id = test.split('/')[3]
    $.ajax({
        url: '/home/my_detail/' + test.split('/')[3] +'/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)

            $('.landlord-name span').html(data.user.name)
            image1 = '<ul class="swiper-wrapper">'
            image3 = '</ul> <div class="swiper-pagination"></div><div class="house-price">￥<span>'+ data.images[0] +'</span>/晚</div>'
            image2 = ''
            for (var i=1; i<data.images.length; i++){

                image2 += '<li class="swiper-slide"><img src="/static/media/' + data.images[i] + '"></li>'
            }
            image = image1 + image2 + image3
            $('.swiper-container').html(image)
            $('.swiper-container').show()
            $('.book-house').attr('href',"/order/booking/"+ id + '/')

//            if (data.pre_order==1){
//                $('.book-house').css({"display":"none"})
//                $('.book-house').hide()
//            }

            html_str = ''
            for (var i=0; i<data.facilities.length; i++){
                html_str += '<li><span class="'+ data.facilities[i].css +'"></span>'+ data.facilities[i].name +'</li>'
            }

            $('#house-facility ul').html(html_str)
//
            $('#house-facility').show()
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })

        },
        error:function(data){
            alert('请求失败')
        }

     })
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();

})
