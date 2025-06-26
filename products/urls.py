from django.urls import path
from .views import ProductListView, ProductDetailView, ManageProductView, CreateProductView, EditProductView, DeleteProductView, DashboardView

urlpatterns = [
    path("shop/", ProductListView.as_view(), name ="shop"),
   
    # Admin Dashboard
    path('manage/', ManageProductView.as_view(), name='manage_products'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('create/', CreateProductView.as_view(), name = 'create_product'),
    path("<slug:slug>/edit/", EditProductView.as_view(), name="edit_product"),
    path('<slug:slug>/delete/', DeleteProductView.as_view(), name='delete_product'),

    # Detail View
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail')
    

]