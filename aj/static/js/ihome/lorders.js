//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
//    $(".order-accept").on("click", function(){
//        var orderId = $(this).parents("li").attr("order-id");
//        $(".modal-accept").attr("order-id", orderId);
//    });

    var path = window.location.pathname
    var id = path.split('/')[3]
    $('.modal-accept').on('click', function(){

        var span = 'WAIT_PAYMENT'
        var orderId = $(".modal-accept").attr("order-id")

//        var order_text = $('.order-title h3').text()
//        var order_id = order_text.split('：')[1]
//        $('.order-text').show()
//        $('.modal-content').hide()
//        console.log(order_id.split('：')[1])
        $.ajax({
            url: '/order/my_orders/'+ id + '/',
            dataType: 'json',
            type: 'POST',
            data:{'statu': span, 'order_id':orderId},
            success:function(data){
                console.log(data)
                location.href = '/order/lorders/'+ id + '/'
            },
            error:function(data){
                alert('请求失败')
            }
        })

    })
//    $(".order-reject").on("click", function(){
//        var orderId = $(this).parents("li").attr("order-id");
//        $(".modal-reject").attr("order-id", orderId);
//
//    });
    $('.modal-reject').on('click', function(){
        var span = 'REJECTED'
        var orderId = $(".modal-reject").attr("order-id")
        var comment = $('#reject-reason').html()
        alert(comment)
//        $('.order-text').show()
//        $('.modal-content').hide()
        $.ajax({
            url: '/order/my_orders/'+ id + '/',
            dataType: 'json',
            type: 'POST',
            data: {'statu': span, 'comment': comment,'order_id': orderId},
            success:function(data){
                console.log(data)
                location.href = '/order/lorders/'+ id + '/'
            },
            error:function(data){
                alert('请求失败')
            }
        })
    })
    var path = window.location.pathname;
    var id = path.split('/')[3]
    $.ajax({
        url: '/order/my_orders/'+ id + '/',
        dataType: 'json',
        type: 'GET',
        success:function(data){
            console.log(data)
            html_str = ''
            for (var i=0; i<data.all_orders.length;i++){
                html_str += '<li order-id="'+ data.all_orders[i].order_id +'"><div class="order-title"><h3>订单编号：'+ data.all_orders[i].order_id +'</h3><div class="fr order-operate">'+
                '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button>'+
                '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button>' +
                '</div></div><div class="order-content"><img src=""><div class="order-text"><h3>'+ data.all_orders[i].house_title +'</h3><ul><li>创建时间：'+ data.all_orders[i].create_date +'</li>'+
                '<li>入住日期：'+ data.all_orders[i].begin_date +'</li><li>离开日期：'+ data.all_orders[i].end_date +'</li><li>合计金额：￥'+ data.all_orders[i].amount +'(共'+ data.all_orders[i].days +'晚)</li><li>订单状态：<span>'+ data.all_orders[i].status +'</span>' +
                '</li><li>客户评价： '+ data.all_orders[i].comment +'</li></ul></div></div></li>'
            }

            $('.orders-list').html(html_str)
            $('.orders-list').show()
            $(".order-accept").on("click", function(){
                console.log('-------------')
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
                console.log(orderId)
            });
            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);

            });

        },
        error:function(data){
            alert('请求失败')
        }
    })
//    $.ajax({
//        url: '/order/my_orders/'+ id + '/',
//        dataType: 'json',
//        type: 'POST',
//        success:function(data){
//            console.log(data)
//        },
//        error:function(data){
//            alert('请求失败')
//        }
//    })
});