
from django.urls import path

from Accounts import views


urlpatterns = [

    path('', views.register, name='register'),

    path('login/', views.loginee, name='login'),
    path('logout/', views.signout, name="logout"),
    path('adminlogin/', views.AdminLogin, name="admin-login"),
    path('Adminpage/', views.AdminPage, name="admin-page"),
    path('Addproduct/', views.AddProduct, name="add-product"),
    path('editproduct/<str:pk>', views.EditProduct, name="edit-product"),
    path('deleteproduct/<str:pk>', views.DeleteProduct, name="delete-product"),
    path('logoutadmin/', views.logoutadmin, name="logout-admin"),
    path('profileadmin/', views.AdminProfile, name="admin-profile"),
    path('user-account/<str:pk>', views.userAccount, name="user-account"),
    path('sendmessage/<str:pk>', views.SendMessage, name="send-message"),
    path('messagecontent/<str:pk>', views.MessageContent, name="message-content"),

    path('readall/', views.ReadAll, name="read-all"),

    path('AddCategory/', views.AddCategory, name="add-category"),
    path('orderrequest/', views.OrderRequest, name="order-request"),







]
