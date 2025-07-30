
# MQ Woodworking – Custom Furniture E-Commerce Site

**Live Site:** https://mq-woodworking.onrender.com

A full-stack e-commerce site built with Django and Python for a real custom furniture business. Features include dynamic product listings, image uploads, cart and checkout functionality with Stripe, and an internal admin dashboard for managing products and orders.

---

## Tech Stack

* Backend: Django, Python, PostgreSQL
* Frontend: Bootstrap, HTMX, HTML/CSS
* Image Hosting: Cloudinary
* Payments: Stripe Checkout
* Deployment: Render
* Authentication: Django’s built-in system

---

## Features

### Public Site

* Dynamic product pages with selectable options (wood type, size, etc.)
* Mobile-responsive design using Bootstrap
* Session-based shopping cart system
* Stripe-powered checkout
* Confirmation and cancel pages after checkout

### Admin Dashboard

* Custom product creation form with:

  * Image uploads to Cloudinary
  * Variant builder (size, wood type, pricing)
  * Rich text descriptions via CKEditor
* Order management system:

  * View customer and order details
  * Update status (In Progress, Completed, Canceled)

---

## Demo Admin Login

You can explore the admin dashboard using:

```
Username: Admin  
Password: Test123
```

Login here:https://mq-woodworking.onrender.com/login/

---

## About the Project

This site was built to replace third-party platforms like Etsy with a custom, scalable solution tailored to the needs of a real furniture business. It allowed me to practice:

* Structuring a Django app for e-commerce
* Integrating APIs like Stripe and Cloudinary
* Managing user sessions and product variation logic
* Deploying and managing production apps on Render

