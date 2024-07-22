from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('with.urls')),  # workhol 앱의 URL들을 포함
    path('calendar/', include('calendar_app.urls')),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

