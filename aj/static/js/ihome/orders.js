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

    var path = window.location.pathname;
    var id = path.split('/')[3]
    console.log(id)
    $.ajax({
        url: '/order/my_orders/' + id + '/',
        dataType: 'json',
        type:'GET',
        success:function(data){
            console.log(data)
            my_orders = ''
            for (var i=0; i<data.all_orders.length; i++){
                    order_title = '<h3>订单编号：'+ data.all_orders[i].order_id +'</h3><div class="fr order-operate"><button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">去支付</button></div><hr>'
                    order_content = '<img style="height:300px;width:400px" src="/static/media/'+ data.all_orders[i].image +'"><div class="order-text"><hr><h3>订单</h3><ul><li>创建时间：'+ data.all_orders[i].create_date +'</li><li>入住日期：'
                    + data.all_orders[i].begin_date +'</li><li>离开日期：'+ data.all_orders[i].end_date + '</li><li>合计金额：'+ data.all_orders[i].amount +'元(共'+ data.all_orders[i].days +'晚)</li><li>订单状态：<span>'+ data.all_orders[i].status +'</span></li><li>我的评价：'+ data.all_orders[i].comment +'</li><li>拒单原因：'+data.all_orders[i].comment+'</li></ul> </div><hr>'
                    my_orders += order_title + order_content

            }
            $('#my_order').html(my_orders)
            $('#my_order').show()

            $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
            $(window).on('resize', centerModals);
            $(".order-comment").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-comment").attr("order-id", orderId);
    });
        },
        error:function(data){
            alert('请求失败')
        }
    })
});