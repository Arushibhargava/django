
from django.urls import path,include

urlpatterns = [
     path('accounts/',include('account.urls')),
     path('home/',include('home.urls'))
]