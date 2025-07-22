from django.urls import path
from .views import HomePageView, AboutPageView, TemplateView, ContactPageView, GalleryPageView,GalleryImageUploadView, GalleryManageView, GalleryImageDeleteView, checkout_cancel, checkout_success
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomePageView.as_view(), name = "home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name = "contact"),
    path('thank-you/', TemplateView.as_view(template_name='thank_you.html'), name='contact_thank_you'),
    path("gallery/", GalleryPageView.as_view(), name ="gallery"),
    path('success/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),



    path("dashboard/gallery-manage/", GalleryManageView.as_view(), name = 'gallery-manage'),
    path("dashboard/gallery-manage/upload/", GalleryImageUploadView.as_view(), name = 'gallery_upload'),
    path("dashboard/gallery-manage/delete/<int:pk>",GalleryImageDeleteView.as_view(), name = 'gallery_delete')
   


]