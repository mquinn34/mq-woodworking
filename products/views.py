from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Product, ProductImage
from django.urls import reverse_lazy
from .forms import ProductForm, ProductVariantFormSet
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

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
        variants = list(self.object.variants.values("id","wood_type", "size", "price_modifier"))
        context["variants"] = variants
        context["wood_options"] = sorted(set(v["wood_type"] for v in variants))
        context["size_options"] = sorted(set(v["size"] for v in variants))
        return context


class ManageProductView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'manage_products.html'
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')


class CreateProductView(LoginRequiredMixin, CreateView):
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

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    variant = form.save(commit=False)
                    variant.product = self.object
                    variant.save()

            for img in images:
                ProductImage.objects.create(product=self.object, image=img)
            return super().form_valid(form) 
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = ProductVariantFormSet(self.request.POST, instance=self.object, prefix='form')
        else:
            formset = ProductVariantFormSet(instance=self.object, prefix='form')

        context['formset'] = formset
        context['empty_form'] = formset.empty_form
        context['existing_images'] = self.object.images.all()
        return context

    def form_valid(self, form):
        formset = ProductVariantFormSet(self.request.POST, instance=self.object, prefix='form')
        images = self.request.FILES.getlist('image')

        if form.is_valid() and formset.is_valid():
            self.object = form.save()

            # Delete removed images
            delete_ids = self.request.POST.getlist('delete_image_ids')
            if delete_ids:
                ProductImage.objects.filter(id__in=delete_ids, product=self.object).delete()

            # Save new images
            for img in images:
                ProductImage.objects.create(product=self.object, image=img)

            # Save all variant forms
            formset.save()

            return redirect('manage_products')

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )



class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'delete_products.html'
    success_url = reverse_lazy('manage_products')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mq_dashboard.html'



