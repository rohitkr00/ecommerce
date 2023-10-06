from django.urls import path
from authcart import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('signupf/',views.signupf,name="signupf"),
    path('verf/',views.OTPverf,name="verf"),
    path('login/',views.handlelogin,name="handlelogin"),
    path('logout/',views.handlelogout,name="handlelogout"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name="activate"),
    


]
