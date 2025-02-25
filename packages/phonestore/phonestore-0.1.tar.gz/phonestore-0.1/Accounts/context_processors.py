

from .models import Message


def message(request):

    counter = 0

    if request.user.is_authenticated:

        Messages = Message.objects.filter(recipient=request.user)
        for mess in Messages:
            counter += 1

    else:

        Messages = None

    return dict(couter=counter)
