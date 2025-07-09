from django.urls import path
from .views import HomePageView, AboutPageView, TemplateView, ContactPageView, GalleryPageView,GalleryImageUploadView, GalleryManageView, GalleryImageDeleteView

urlpatterns = [
    path("", HomePageView.as_view(), name = "home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name = "contact"),
    path('thank-you/', TemplateView.as_view(template_name='thank_you.html'), name='contact_thank_you'),
    path("gallery/", GalleryPageView.as_view(), name ="gallery"),


    path("dashboard/gallery-manage/", GalleryManageView.as_view(), name = 'gallery-manage'),
    path("dashboard/gallery-manage/upload/", GalleryImageUploadView.as_view(), name = 'gallery_upload'),
    path("dashboard/gallery-manage/delete/<int:pk>",GalleryImageDeleteView.as_view(), name = 'gallery_delete')
   


]