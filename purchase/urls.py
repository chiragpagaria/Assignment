"""assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from purchase import views
from purchase.views import ChartData

urlpatterns = [
    # url(r'^home', purchase_data.as_view(), name='api-data'),
    url(r'^home', views.purchase_data, name='views-purchase_data'),
    # url(r'^api/chart/data/', views.ChartData, name='api-data'),
    url(r'^api/chart/data/', ChartData.as_view(), name='api-data'),
]
