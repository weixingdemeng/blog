from django.core.paginator import Paginator
from django.shortcuts import render

from fresh_shop.settings import ORDER_NUMBER2
from goods.models import Goods, GoodsCategory


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # 组织结果的对象objects:包含分类，该分类的前四个商品信息
        # 方式1：object ==>[GoodsCategory Object, [Goods object1,...Goods object6]]
        categorys = GoodsCategory.objects.all()

        goods = Goods.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]

            # print(goods)
            data = [category, goods]
            result.append(data)
        # print(result)
        # 方式2：object==>{'category_name':[Goods object1,...Goods object6]}

        # indexs = []
        # goods = []
        # shop_prices = []
        # goods_c = GoodsCategory.objects.all()
        # for good_c in goods_c:
        #     indexs.append(good_c.category_type)
        # for index in indexs:
        #
        #     goods_front_images = []
        #     goods_q = Goods.objects.filter(category=index)
        #     for goods_g in goods_q:
        #         goods.append(goods_g.name)
        #         shop_prices.append(goods_g.shop_price)
        #         goods_front_images.append(goods_g.goods_front_image)
        return render(request, 'index.html',{'result': result, 'category_type': category.CATEGORY_TYPE})


def detail(request, id):
    if request.method == 'GET':
        # 返回详情页面解析的商品信息
        session_goods = request.session.get('goods')
        if not session_goods:
            session_goods = []
        new_good = [id, 1 ,1]
        goods = Goods.objects.filter(pk=id).first()
        session_goods.append(new_good)
        return render(request, 'detail.html', {'goods': goods})


def list(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        goods_category = GoodsCategory.objects.all()
        all_goods = Goods.objects.all()
        pg = Paginator(all_goods, ORDER_NUMBER2)
        all_goods = pg.page(page)
        for categorys in goods_category:
            category = categorys.category_type
            return render(request, 'list.html',{'all_goods':all_goods, 'category':category})