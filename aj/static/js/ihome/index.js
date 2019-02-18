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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/user/search/?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));

    aid = $(th).attr("area-id")
    aname = areaName
    sd = $(th).attr("start-date")
    ed = $(th).attr("end-date")
    url_list = [aid, aname, sd, ed]

    $.ajax({
        url:'/user/my_index/',
        dataType: 'json',
        type: 'POST',
        data:{'aid': aid, 'aname': aname, 'sd': sd, 'ed': ed},
        success:function(data){
            console.log(data)
            location.href = url;
        },
        error:function(data){
            alert('请求失败')
        }
    })
}

$(document).ready(function(){
    $(".top-bar>.register-login").show();
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    }); 
//    $(".area-list a").click(function(e){
//        $("#area-btn").html($(this).html());
//        $(".search-btn").attr("area-id", $(this).attr("area-id"));
//        $(".search-btn").attr("area-name", $(this).html());
//        $("#area-modal").modal("hide");
//    });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
    $.ajax({
        url: '/user/my_index/',
        type: 'GET',
        dataType:'json',
        success:function(data){
             console.log(data);
            if (data.username){
                text = '<a style="font-size:15px;margin-right:10px">用户名：'+ data.username +'</a><a style="font-size:15px;color:red" onclick="logout()">退出<a/>'
                $('.register-login').html(text)
                $('.register-login').show()
            }
            swiper_slide = ''
            for (var i=0; i<data.image_list.length; i++){
                swiper_slide += '<div class="swiper-slide"> <a><img style="height:200px;width:400px" src="/static/media/'+ data.image_list[i] +'"></a><div class="slide-title">房屋标题1</div></div>'
            }
            $('.swiper-wrapper').html(swiper_slide)
            $('.swiper-wrapper').show()
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            area_list = ''
            for (i=0; i<data.areas.length-1;i++){
                area_list += '<a href="#" area-id="'+ data.areas[i].id +'">'+ data.areas[i].name +'</a>'
            }
            $('.area-list').html(area_list)
                $('.area-list').show()
            $(".area-list a").click(function(e){

                $("#area-btn").text($(this).text());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).text());
                $("#area-modal").modal("hide");
            });


        },
        error:function(data){
            alert('请求失败')
        }
    })
})
function logout(){
    $.ajax({
        url:'/user/logout/',
        type: 'POST',
        dataType:'json',
        success:function(data){
            location.href = '/user/index/'
        },
        error:function(data){
            alert('退出登录失败')
        }

    })
}