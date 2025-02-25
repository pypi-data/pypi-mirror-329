from django.urls import path

from phone import views


urlpatterns = [

    path('', views.home, name='home-page'),
    path('store/', views.store, name='store-page'),
    path('pricerange/', views.pricerange, name='price-range'),

    path('caegory/<str:pk>', views.categoryProduct, name='category-product'),
    path('productdetail/<str:pk>', views.Productdetail, name='product-detail'),



]
