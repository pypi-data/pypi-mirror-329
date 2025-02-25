from django.shortcuts import redirect, render

from .models import Product, Category
# Create your views here.


def home(request):

    product = Product.objects.all()

    context = {"product": product}

    return render(request, 'phones/index.html', context)


def store(request):

    products = Product.objects.all()

    category = Category.objects.all()

    counter = products.count()

    context = {"products": products, 'category': category, "counter": counter}

    return render(request, 'phones/store.html', context)


def pricerange(request):

    if request.method == "POST":

        price = request.POST['price']

        productss = Product.objects.filter(Price=price)

        category = Category.objects.all()

        counter = productss.count()

    else:

        return redirect("store-apge")

    context = {"products": productss, 'category': category, "counter": counter}

    return render(request, 'phones/storePrices.html', context)


def categoryProduct(request, pk):

    category = Category.objects.all()

    categoryproduct = Category.objects.get(id=pk)

    donc = Product.objects.filter(category=categoryproduct)
    counter = donc.count()

    context = {"donc": donc, 'category': category, "counter": counter}

    return render(request, 'phones/categoryproduct.html', context)


def Productdetail(request, pk):

    product_detail = Product.objects.get(id=pk)

    context = {"productD": product_detail}

    return render(request, 'phones/product_detail.html', context)
