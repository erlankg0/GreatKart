from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

"""Главный маршрутизатор/ Main URL"""
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('store.urls')),  # приложения store
                  path('cart/', include('cart.urls')),  # приложения cart (корзина)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # URL MEDIA
