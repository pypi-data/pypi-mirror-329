from django.urls import path


from orders import views


urlpatterns = [


    path('', views.CheckOut, name='checkout'),
    path('payement/', views.payement, name='payement'),
    path('sucess/', views.OrederSucces, name='order-success'),

    path('sucessorder/', views.Sucess, name='success'),




]
