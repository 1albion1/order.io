from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from main.views import handle_not_found
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls',namespace="main")),
    path('manager/', include('manager.urls',namespace="manager")),
    path('employee/', include('employee.urls',namespace="employee")),
    path('account/', include('account.urls')),
    path('order/', include('order.urls',namespace="order")),
    path('menu/', include('menu.urls',namespace="menu")),
    path('meal/', include('meal.urls',namespace="meal")),
    path('notification/', include('notification.urls',namespace="notification")),
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.handle_not_found'
