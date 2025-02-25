from django.shortcuts import render, redirect

from card.models import CardItem
from datetime import date
from datetime import datetime
from orders.models import Order, OrderProduct
from .forms import OrderForm
# Create your views here.


def CheckOut(request, total=0, quantity=0):

    grand_total = 0

    tax = 0

    cartitem = CardItem.objects.filter(owner=request.user)

    for cartitems in cartitem:

        total += (cartitems.quantity * cartitems.product.Price)
        quantity += cartitems.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    orderform = OrderForm()

    if request.method == "POST":
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            orderforms = orderform.save(commit=False)
            orderforms.user = request.user
            orderforms.order_total = grand_total
            orderforms.tax = tax
            orderforms.ip = request.META.get('REMOTE_ADDR')

            orderforms.save()

            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr, mt, dt)

            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(orderforms.id)
            orderforms.order_number = order_number

            orderforms.save()

            order = Order.objects.get(order_number=order_number)

            context = {"order": order, "cartitem": cartitem,
                       "grand_total": grand_total, "quantity": quantity, "tax": tax, "total": total}

            return render(request, 'payement.html', context)

    context = {"orderform": orderform, "cartitem": cartitem,

               "grand_total": grand_total, "quantity": quantity, "tax": tax, "total": total}

    return render(request, 'checkout.html', context)


def payement(request):

    return render(request, 'payement.html')

def OrederSucces(request):

    profile = request.user

    cardtitem = CardItem.objects.filter(owner=profile)

    order_num = request.GET.get('ordernum')

    order = Order.objects.get(order_number=order_num,
                              user=request.user, is_ordered=False)

    for cartitem in cardtitem:

        orderproduct = OrderProduct()
        orderproduct.order = order
        orderproduct.user = request.user
        orderproduct.product = cartitem.product
        orderproduct.product_owner = cartitem.product.owner
        orderproduct.quantity = cartitem.quantity
        orderproduct.product_price = cartitem.product.Price
        orderproduct.ordered = True
        orderproduct.save()

    CardItem.objects.filter(owner=request.user).delete()

    return redirect('success')
    
def Sucess(request):

    orderProduct = OrderProduct.objects.filter(user=request.user)

    grand_total = 0
    total = 0
    tax = 0
    for order in orderProduct:

        total += order.product_price * order.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {"orderproduct": orderProduct, "total": total,
               "tax": tax, "grand_total": grand_total}

    return render(request, 'sucess.html', context)
