from django.urls import path

from card import views


urlpatterns = [

    path('', views.cart, name='card'),

    path('add/<str:pk>', views.addtocard, name='addto-card'),

    path('RemoveItem/<str:pk>', views.removeItem, name='remove-item'),

    path('MinusItem/<str:pk>', views.MinusItem, name='minus-item'),

    path('PlusItem/<str:pk>', views.PlusItem, name='Plus-item'),

    path('checkout/', views.CheckOut, name='checkout'),


]
