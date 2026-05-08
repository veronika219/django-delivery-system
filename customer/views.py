from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from customer.models import MenuItem, OrderModel, Category


def index(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "customer/index.html")


def about(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "customer/about.html")


class Menu(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # get categories
        categories = Category.objects.all().prefetch_related("items")

        # pass into context
        context = {
            "categories": categories,
        }

        # render the template
        return render(request, "customer/menu.html", context=context)

    # def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     order_items = {
    #         'items': []
    #     }
    #
    #     items = self.request.POST.getlist('items[]')
    #     for item in items:
    #         menu_item = MenuItem.objects.get(pk=int(item))
    #         item_data = {
    #             'id': menu_item.pk,
    #             'name': menu_item.name,
    #             'price': menu_item.price
    #         }
    #         order_items["items"].append(item_data)
    #
    #     price = 0
    #     item_ids = []
    #
    #     for item in order_items['items']:
    #         price += item['price']
    #         item_ids.append(item['id'])
    #
    #     order = OrderModel.objects.create(price=price)
    #     order.items.add(*item_ids)
    #
    #     context = {
    #         # список товарів
    #         'items': order_items['items'],
    #         # загальна ціна
    #         'price': price,
    #     }
    #
    #     return render(request, "customer/order_confirmation.html", context=context)
