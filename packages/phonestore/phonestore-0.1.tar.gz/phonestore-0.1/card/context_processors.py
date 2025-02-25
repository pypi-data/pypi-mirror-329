from .models import CardItem


def quant(request):

    quantities = 0

    if request.user.is_authenticated:

        linkss = CardItem.objects.filter(owner=request.user)

        for cartitem in linkss:

            quantities += cartitem.quantity
            
    else:

        linkss = None

    return dict(quantities=quantities)
