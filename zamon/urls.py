from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  
    path('detail/<int:pk>/', detail, name='detail'),
    path('category/<int:pk>/', category_detail, name='category'),
    path('likecomment/<int:pk>/', like_comment, name='like_comment'),
    path('contact/', contact, name='contact'),  
    path('about/', about, name='about'),
    path('interface/', interface, name='interface'),
    path('editcomment/<int:pk>/', edit_comment, name='edit_comment'),
    path('deletecomment/<int:pk>/', delete_comment, name='delete_comment'),
    path('user/', include('user.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)