from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls',namespace="main")),
    path('manager/', include('manager.urls',namespace="manager")),
    path('employee/', include('employee.urls',namespace="employee")),
    path('account/', include('account.urls')),
    path('order/', include('order.urls',namespace="order")),
    path('menu/', include('menu.urls',namespace="menu")),
    path('meal/', include('meal.urls',namespace="meal")),
    #path('reports/', include('reports.urls',namespace="reports"))
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)