function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
function submit_order(){
    var house_title = $('.house-text h3').html()
    var start_time = $('#start-date').val()
    var end_time = $('#end-date').val()
    var path = window.location.pathname;
    var id = path.split('/')[3]
    $.ajax({
        url: '/order/my_booking/'+ id + '/',
        type: 'POST',
        data: {'house_title': house_title, 'start_time': start_time, 'end_time': end_time},
        dataType: 'json',
        success:function(data){
            console.log(data)
            if(data.success == 1){
                location.href = '/order/orders/' + data.user_id + ''
            }
            else{
                alert('创建订单失败,您选择的时间期间该房屋已被下单，请重新选择时间段，或者对其他房屋进行下单')
            }
        },
        error:function(data){
            alert('请求失败')
        }
    })
}
$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var path = window.location.pathname;
    var id = path.split('/')[3]
    $.ajax({
        url: '/order/my_booking/'+ id +'/',
        type: 'GET',
        dataType: 'json',
        success:function(data){
            console.log(data)
            $('.house-info img').attr('src', '/static/media/' + data.house.image)
//            $('<image src="/static/media/'+ data.house.image + '">')
//            $('.house-info').html('<image src="/static/media/'+ data.house.image + '">')
            $('.house-text h3').html(data.house.title)
            $('.house-text span').html(data.house.price)
            $('.house-text').show()


        },
        error:function(data){
            alert('请求失败')
        }
    })
})
