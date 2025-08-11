from django.urls import path
from home.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    #path('login/', LoginInterfaceView.as_view(), name = 'login'),
    #path('logout/', LogoutInterfaceView.as_view(),name = "logout"),
]