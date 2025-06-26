from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Product, ProductImage
from django.urls import reverse_lazy
from .forms import ProductForm, ProductVariantFormSet
from django.shortcuts import redirect

class ProductListView(ListView):
    model = Product
    template_name = "shop.html"
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = self.object.images.all()
        variants = list(self.object.variants.values("wood_type", "size", "price_modifier"))
        context["variants"] = variants
        context["wood_options"] = sorted(set(v["wood_type"] for v in variants))
        context["size_options"] = sorted(set(v["size"] for v in variants))
        return context


class ManageProductView(ListView):
    model = Product
    template_name = 'manage_products.html'
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_products.html'
    success_url = reverse_lazy('manage_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = ProductVariantFormSet(self.request.POST, prefix='form')
        else:
            formset = ProductVariantFormSet(prefix='form')

        context['formset'] = formset
        context['empty_form'] = ProductVariantFormSet(prefix='form').empty_form
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        images = self.request.FILES.getlist('image')
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            for img in images:
                ProductImage.objects.create(product=self.object, image=img)
            return super().form_valid(form) 
        else:
            return self.render_to_response(self.get_context_data(form=form))



class EditProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_products.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = ProductVariantFormSet(self.request.POST, instance=self.object)
        else:
            formset = ProductVariantFormSet(instance=self.object)

        context['formset'] = formset
        context['empty_form'] = formset.empty_form
        context['existing_images'] = self.object.images.all() 

        return context

    def form_valid(self, form):
    # bind the formset to POST + current instance
        formset = ProductVariantFormSet(self.request.POST, instance=self.object)
        images = self.request.FILES.getlist('image')
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            delete_ids = self.request.POST.getlist('delete_image_ids')
            if delete_ids:
                ProductImage.objects.filter(id__in=delete_ids, product=self.object).delete()

            for img in images:
                ProductImage.objects.create(product=self.object, image=img)
            return redirect('manage_products')

    # if anything is invalid, fall through and show the form again
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
    )


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'delete_products.html'
    success_url = reverse_lazy('manage_products')



class DashboardView(TemplateView):
    template_name = 'mq_dashboard.html'



