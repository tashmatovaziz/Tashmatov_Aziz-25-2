"""onlineStore URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import hello, goodby, now_date, MainPageCBV, ProductsCBV, hashtags, product_detail_view, \
    CreateProductsCBV
from django.conf.urls.static import static
from onlineStore import settings
from users.views import register_view, login_view, logout_veiw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('now_date/', now_date),
    path('goodby/', goodby),
    path('', MainPageCBV.as_view(template_name='layouts/index.html')),
    path('products/', ProductsCBV.as_view()),
    path('hashtags/', hashtags),
    path('products/<int:id>/', product_detail_view),
    path('products/create/', CreateProductsCBV.as_view()),
    path('users/register/', register_view),
    path('users/login/', login_view),
    path('users/logout/', logout_veiw),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)