from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("gallery/", views.MediaGalleryView.as_view(), name="gallery"),
    path("search/", views.MediaSearchView.as_view(), name="search"),
    path("upload/", views.MediaUploadView.as_view(), name="upload media"),
    path(
        "upload/success/", views.MediaUploadSuccessView.as_view(), name="upload success"
    ),
    path("media-creation/", views.MediaCreateView.as_view(), name="create media"),
    path("<str:slug>/", views.MediaDetailView.as_view(), name="detail media"),
    path("<str:slug>/delete/", views.MediaDeleteView.as_view(), name="delete media"),
    path("<str:slug>/update/", views.MediaUpdateView.as_view(), name="update media"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
