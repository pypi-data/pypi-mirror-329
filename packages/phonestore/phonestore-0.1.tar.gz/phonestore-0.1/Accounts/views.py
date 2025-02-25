from multiprocessing import context
from django.shortcuts import redirect, render

from .models import Account, Message
from .forms import registerForm, formmessage
from django.contrib.auth.decorators import login_required

from phone.models import Product
from orders.models import OrderProduct
from .forms import Categoryform
from django.contrib.auth import login, logout, authenticate
from phone.forms import ProductForm
# Create your views here.


def register(request):

    if request.method == "POST":

        register = registerForm(request.POST, request.FILES)

        if register.is_valid():
            first_name = register.cleaned_data['first_name']
            last_name = register.cleaned_data['last_name']
            phone_number = register.cleaned_data['phone_number']
            email = register.cleaned_data['email']
            profile_image = register.cleaned_data['profile_image']

            password = register.cleaned_data['password']

            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.profile_image = profile_image
            user.save()
            return redirect("home-page")

    register = registerForm()

    context = {"register": register}

    return render(request, 'register.html', context)


def loginee(request):

    if request.method == "POST":

        email = request.POST['email']

        password = request.POST['password']

        user = Account.objects.get(email=email)

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:

            login(request, user)

            return redirect("home-page")

        else:

            return redirect("login")

    return render(request, 'login.html')


def signout(request):

    logout(request)

    return redirect("login")


def AdminLogin(request):

    if request.method == "POST":

        email = request.POST['email']

        password = request.POST['password']

        user = Account.objects.get(email=email)

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active and user.is_admin:

            login(request, user)

            return redirect("admin-page")

        else:

            return redirect("admin-login")

    return render(request, 'adminlogin.html')


def AdminPage(request):

    profile = request.user

    product = Product.objects.filter(owner=profile)

    message = Message.objects.filter(recipient=profile)

    context = {"pro": product, "message": message}

    return render(request, 'AdminPage.html', context)


def AddProduct(request):

    form = ProductForm()

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            forms = form.save(commit=False)

            forms.owner = request.user
            forms.save()
            return redirect('admin-page')

    context = {"form": form}

    return render(request, 'addProduct.html', context)


def EditProduct(request, pk):

    product = Product.objects.get(id=pk)

    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("admin-page")

    context = {"form": form}

    return render(request, 'editProduct.html', context)


def DeleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("admin-page")


def logoutadmin(request):
    logout(request)
    return redirect("admin-login")


def AdminProfile(request):

    profile = Account.objects.filter(is_admin=True)

    context = {"profile": profile}

    return render(request, 'Profiles.html', context)


def userAccount(request, pk):

    profile = Account.objects.get(id=pk)

    product = Product.objects.filter(owner=profile)

    context = {"profile": profile, "product": product}

    return render(request, 'useraccount.html', context)


@login_required(login_url="login")
def SendMessage(request, pk):

    profile = Account.objects.get(id=pk)

    form = formmessage()

    if request.method == "POST":
        form = formmessage(request.POST)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.sender = request.user
            forms.recipient = profile
            forms.save()
            return redirect("user-account", pk)

    context = {"form": form}

    return render(request, 'sendmessage.html', context)


def MessageContent(request, pk):

    messag = Message.objects.get(id=pk)
    messag.is_read = True
    messag.save()

    message = Message.objects.filter(recipient=request.user)

    context = {"messag": messag, "message": message}

    return render(request, 'messagecontent.html', context)


def ReadAll(request):

    message = Message.objects.filter(recipient=request.user)

    counters = Message.objects.filter(is_read=False)

    counter = counters.count()

    context = {"mess": message, "counter": counter}

    return render(request, 'inbox.html', context)


def AddCategory(request):

    catform = Categoryform()

    if request.method == "POST":

        catform = Categoryform(request.POST)

        if catform.is_valid():

            catform.save()

            return redirect("admin-page")

    context = {"formCat": catform}

    return render(request, "AddCategory.html", context)



def OrderRequest(request):


    
    message = Message.objects.filter(recipient=request.user)

    orderproduct = OrderProduct.objects.filter(product_owner = request.user)
    
    context = { "message": message,"orderproduct":orderproduct}


    return render(request, 'OrederRequest.html', context)
