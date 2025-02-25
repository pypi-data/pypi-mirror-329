from multiprocessing import context
from django.shortcuts import redirect, render

from phone.models import Product

from .models import CardItem

from django.contrib.auth.decorators import login_required


# Create your views here.

def cart(request):

    total = 0

    if request.user.is_authenticated:

        cartitem = CardItem.objects.filter(owner=request.user)


        for cartitems in cartitem:


            total += (cartitems.quantity * cartitems.product.Price)


        tax = (2 * total) / 100

        grand_total = total + tax

    else:


        cartitem = None


    context = {"cartitem": cartitem, "total": total,
               "tax": tax, "grand_total": grand_total}


    return render(request, 'cards/addto.html', context)



@login_required(login_url="login")

def addtocard(request, pk):

    product = Product.objects.get(id=pk)

    try:

        cartitem = CardItem.objects.get(product=product, owner=request.user)

        cartitem.quantity = cartitem.quantity + 1

        cartitem.totals = cartitem.quantity * cartitem.product.Price

        cartitem.save()

        return redirect("card")


    except:

        cartitem = CardItem.objects.create(

            owner=request.user, product=product, quantity=1,

            totals=1

        )


        cartitem.totals = cartitem.quantity * cartitem.product.Price

        cartitem.save()

        return redirect("card")


def removeItem(request, pk):

    cartItem = CardItem.objects.get(id=pk)

    cartItem.delete()

    return redirect("card")


def MinusItem(request, pk):

    cartitems = CardItem.objects.get(id=pk)

    if cartitems.quantity <= 1:

        cartitems.delete()

        return redirect("card")

    else:

        cartitems.quantity -= 1
        cartitems.totals = cartitems.quantity * cartitems.product.Price

        cartitems.save()

        return redirect("card")


def PlusItem(request, pk):

    cartitem = CardItem.objects.get(id=pk)

    cartitem.quantity += 1

    cartitem.totals = cartitem.quantity * cartitem.product.Price

    cartitem.save()

    return redirect("card")


def CheckOut(request):

    return render(request, 'cards/checkout.html')
