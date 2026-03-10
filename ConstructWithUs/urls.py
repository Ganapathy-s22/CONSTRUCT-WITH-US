"""
URL configuration for ConstructWithUs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Construct import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index),
    path('home/', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('services/',views.services,name='services'),

    path('ag_dashboard/',views.ag_dashboard,name='agency_dash'),
    path('agency_signup/',views.signup_agy,name='agy_signup'),
    path('agency_login/',views.login_agy,name='agy_login'),
    path('agency_logout/',views.agency_logout,name='agency_logout'),
    path('agency_profile/',views.agency_profile,name='agency_profile'),
    path('agency_products/',views.ag_products,name='agency_products'),
    path('agency_all_products/',views.agency_all_products,name='agency_all_products'),

    path("agency/manage-quotations/",views.manage_requested_replies,name="manage_requested_replies"),
    path("quotation/<int:quotation_id>/bill/",views.products_quotation_page,name="products_quotation_page"),
    path(
    "quotation/<int:quotation_id>/update-status/",
    views.update_quotation_status,
    name="update_quotation_status"
),
path(
    "agency/generate-final-bill/<int:quotation_id>/",
    views.generate_final_bill,
    name="generate_final_bill"
),
path(
    "agency/show-final-bill/<int:quotation_id>/",
    views.agency_show_final_bill,
    name="agency_show_final_bill"
),
path(
    "agency/orders/",
    views.agency_orders,
    name="agency_orders"
),
path(
    "agency/order/<int:order_id>/update-status/",
    views.agency_update_order_status,
    name="agency_update_order_status"
),

path(
    "agency/order/<int:order_id>/dispatch/",
    views.agency_dispatch_order,
    name="agency_dispatch_order"
),









    path("product_edit/",views.edit_delete_product,name="edit_delete_product"),
    path("product/edit/<int:product_id>/",views.edit_product,name="agency_edit_product"),
    path("product/delete/<int:product_id>/", views.delete_product, name="agency_delete_product"),
    path("variant/delete/<int:variant_id>/", views.delete_variant,name="agency_delete_variant"),
    path("product/delete-confirm/<int:product_id>/",views.delete_product_confirm,name="agency_delete_product_confirm"),

    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    path("check-phone/", views.check_phone, name="check_phone"),
    path("check-company-phone/", views.check_company_phone, name="check_company_phone"),
    path("check-owner-phone/", views.check_owner_phone, name="check_owner_phone"),
    path("check-gst/", views.check_gst, name="check_gst"),

    path('eng_signup/',views.engsignup,name='eng_signup'),
    path('eng_login/',views.englogin,name='eng_login'),
    path('eng_dash/',views.eng_dashboard,name='eng_dash'),
    path('eng_profile/',views.engineer_profile,name='eng_profile'),
    path('create_site/',views.create_site,name='create_site'),
    path('manage_all_site/',views.all_sites,name='manage_all_site'),
    path("site/details/<int:site_id>/",views.site_details,name="site_details"),
    path("edit-site/<int:site_id>/",views.edit_site_details,name="edit_site_details"),


    path("products/", views.all_products, name="all_products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/", views.edit_product, name="edit_product"),
    path("product-variations/", views.add_product_variation, name="add_product_variation"),

    path('edit_delete_site/',views.edit_delete_site,name='edit_delete_site'),
    path("delete-site/<int:site_id>/",views.delete_site,name="delete_site"),
    path("site/<int:site_id>/materials/",views.manage_site_construction_materials,name="manage_site_materials"),

    path("site/<int:site_id>/search-products/",views.search_products,name="search_products"),
    path("site/<int:site_id>/add-to-cart/<int:variant_id>/",views.add_to_cart,name="add_to_cart"),
    path("site/<int:site_id>/cart/",views.view_cart,name="view_cart"),

    path("site/<int:site_id>/cart/remove/<int:item_id>/", views.remove_cart_item,name="remove_cart_item"),

    path("site/<int:site_id>/quotation/single/<int:item_id>/",views.request_single_quotation,name="request_single_quotation"),
    path("site/<int:site_id>/quotation/full/",views.request_full_quotation,name="request_full_quotation"),
    path("quotation/<int:quotation_id>/",views.view_quotation_invoice,name="view_quotation_invoice"),

    path("site/<int:site_id>/manage-quotations-orders/",views.manage_quotations_orders, name="manage_quotations_orders"),
    path( "final-bill/<int:quotation_id>/",views.final_view_bill,name="final_view_bill"),
    path("place-order/<int:quotation_id>/",views.place_order,name="place_order"),
    path("payment/<int:quotation_id>/",views.payment_page,name="payment_page"),
    path("confirm-cod/<int:quotation_id>/",views.confirm_cod_order,name="confirm_cod_order"),
    path(
    "order-success/<int:site_id>/",
    views.order_success_page,
    name="order_success_page"
),
path(
    "site/<int:site_id>/confirmed-orders/",
    views.confirmed_orders,
    name="confirmed_orders"
),
path(
    "agency-order-bill/<int:order_id>/",
    views.agency_order_bill,
    name="agency_order_bill"
),

path(
    "agency-dispatch-order/<int:order_id>/",
    views.agency_dispatch_order,
    name="agency_dispatch_order"
),


    path("engineer/logout/", views.engineer_logout, name="engineer_logout"),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)