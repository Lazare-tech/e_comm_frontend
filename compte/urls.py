from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
import compte.views
#

# path('',LoginView.as_view(template_name='compte/login.html',
#                           redirect_authenticated=True),
#      name='login'),
# path('logout/',LogoutView.as_view(),name='logout')
app_name= "compte"
urlpatterns = [
    path('login/',compte.views.login_page,name='login'),
    path('signup/',compte.views.signup_page,name='signup'),
    path('logout/',compte.views.logout_user,name='logout')
]
