from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView
from django.views.generic.edit import FormView
from products.models import Product
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import GalleryImage
from django.db.models import Min
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(ListView):
    model = Product
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = Product.objects.filter(is_featured=True).annotate(
            min_price= Min('variants__price_modifier'))[:3]
        context['featured_products'] = featured
        return context

class AboutPageView(TemplateView):
    template_name = "about.html"

class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_thank_you')

    def form_valid(self, form):
        # Grab form data
        first = form.cleaned_data['first_name']
        last = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone_number']
        message = form.cleaned_data['message']

        # Build email message
        full_message = f"""
        MQ Woodworking Contact Form Submission

        Name: {first} {last}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        # Send email
        send_mail(
            subject='New Contact Form Submission',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['mqwoodworking@gmail.com'],
        )

        return super().form_valid(form)


class GalleryImageUploadView(LoginRequiredMixin, View):
    template_name = 'gallery_upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        images = request.FILES.getlist('image')  
        for img in images:
            GalleryImage.objects.create(image=img)
        return redirect('gallery-manage')



class GalleryManageView(LoginRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'gallery_manage.html'
    context_object_name = 'images'
    ordering = ['-uploaded_at']

class GalleryImageDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryImage
    template_name = 'gallery_confirm_delete.html'
    success_url = reverse_lazy('gallery-manage')


class GalleryPageView(ListView):
    model = GalleryImage
    template_name = "gallery.html"
    context_object_name = "images"
    ordering = ["-uploaded_at"]

def checkout_success(request):
    return render(request, "checkout_success.html")

def checkout_cancel(request):
    return render(request, "checkout_cancel.html")





