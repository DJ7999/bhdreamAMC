from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/",include("user_controller.urls")),
    path("portfolio/",include("portfolio_controller.urls")),
    path("wealthwish/",include("wealthwish_controller.urls"))
]
