from django.contrib import admin
from . models import * 

# Register your models here.
from django.contrib import admin
from .models import Engineerprofile, AgencyProfile, Product, ProductVariants


# ================= ENGINEER =================
@admin.register(Engineerprofile)
class EngineerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "degree",
        "college_name",
        "full_name",
        "phone_number",
        "district",
        "state",
        "pincode",
        "created_at",
    )
    search_fields = ("user__username", "email", "phone_number")
    list_filter = ("degree", "gender", "state")


# ================= AGENCY =================
@admin.register(AgencyProfile)
class AgencyAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "gst_number",
        "company_phone",
        "owner_name",
        "owner_email",
        "owner_phone",
        "company_district",
        "company_state",
        "company_pincode",
        "status",
        "approved_at",
    )
    search_fields = ("company_name", "gst_number", "owner_name")
    list_filter = ("status", "company_state")


# ================= PRODUCT =================
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "agency",
        "product_type",
        "display_product_type",
        "brand_name",
        "product_name",
        "pincode",
        "created_at",
    )

    list_filter = (
        "product_type",
        "pincode",
        "agency__company_district",
    )

    search_fields = (
        "brand_name",
        "product_name",
        "address",
        "pincode",
        "agency__company_name",
    )

    ordering = ("-created_at",)

    list_per_page = 20


    # 🔥 Show correct product type (including Others custom name)
    def display_product_type(self, obj):
        if obj.product_type == "others" and obj.other_product_type:
            return obj.other_product_type
        return obj.get_product_type_display()

    display_product_type.short_description = "Product Type"



# ================= PRODUCT VARIANTS =================
from django.contrib import admin
from .models import ProductVariants


@admin.register(ProductVariants)
class ProductVariantsAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "spc_product_name",
        "size_or_weight",
        "unit",
        "price",
        "stock",
        "is_active",
        "created_at",
    )

    list_filter = (
        "unit",
        "is_active",
        "product__product_type",
    )

    search_fields = (
        "product__brand_name",
        "product__product_name",
        "spc_product_name",
    )

    ordering = ("-created_at",)

    list_editable = (
        "price",
        "stock",
        "is_active",
    )


from django.contrib import admin
from .models import ConstructionSite, SiteOwner


# ===============================
#   Construction Site Admin
# ===============================

from django.utils.html import format_html

@admin.register(ConstructionSite)
class ConstructionSiteAdmin(admin.ModelAdmin):

    list_display = (
        "site_name",
        "engineer",
        "category",
        "other_category",
        "status",
        "total_sqft",
        "site_district",
        "site_pincode",
        "view_site_map",
        "view_blueprint",
        "description",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "site_district",
        "site_state",
        "created_at",
    )

    search_fields = (
        "site_name",
        "site_district",
        "site_pincode",
        "engineer__username",
    )

    ordering = ("-created_at",)

    # 🔥 Custom column for Site Map
    def view_site_map(self, obj):
        if obj.site_map:
            return format_html(
                '<a href="{}" target="_blank">View Map</a>',
                obj.site_map.url
            )
        return "No File"

    view_site_map.short_description = "Site Map"


    # 🔥 Custom column for Blueprint
    def view_blueprint(self, obj):
        if obj.blueprint_file:
            return format_html(
                '<a href="{}" target="_blank">View Blueprint</a>',
                obj.blueprint_file.url
            )
        return "No File"

    view_blueprint.short_description = "Blueprint"


# ===============================
#   Site Owner Admin
# ===============================

@admin.register(SiteOwner)
class SiteOwnerAdmin(admin.ModelAdmin):

    list_display = (
        "owner_name",
        "site",
        "owner_gender",
        "owner_phone",
        "owner_district",
        "owner_pincode",
    )

    list_filter = (
        "owner_gender",
        "owner_district",
    )

    search_fields = (
        "owner_name",
        "owner_phone",
        "site__site_name",
    )


from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "site",
        "product_name",
        "weight_or_size",
        "average_price",
        "quantity",
        "created_at",
    )
    list_filter = ("created_at", "site")
    search_fields = ("product_name",)

from django.contrib import admin
from .models import QuotationRequest, QuotationItem


# 🔹 Inline Items (QuotationItem inside QuotationRequest)
class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0
    readonly_fields = ("product_name", "weight_or_size", "quantity", "price")


# 🔹 Main QuotationRequest Admin
@admin.register(QuotationRequest)
class QuotationRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "site",
        "engineer",
        "agency",
        "estimated_total",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "agency",
    )

    search_fields = (
        "id",
        "site__site_name",
        "engineer__username",
        "agency__company_name",
    )

    readonly_fields = (
        "created_at",
        "estimated_total",
    )

    inlines = [QuotationItemInline]

    ordering = ("-created_at",)


# 🔹 Separate QuotationItem Admin (optional)
@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):

    list_display = (
        "quotation",
        "product_name",
        "weight_or_size",
        "quantity",
        "price",
    )

    search_fields = (
        "product_name",
        "quotation__id",
    )

from django.contrib import admin
from .models import EstimatedQuotation




# admin.py

from django.contrib import admin
from .models import Order, OrderItem, OrderDelivery


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderDeliveryInline(admin.StackedInline):
    model = OrderDelivery
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "engineer",
        "agency",
        "total_amount",
        "payment_method",
        "cod_confirmed",
        "order_status",
        "created_at",
    )
    list_filter = ("order_status", "payment_method", "cod_confirmed")
    search_fields = ("id", "engineer__username")
    inlines = [OrderItemInline, OrderDeliveryInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "quantity", "price", "total_price")


@admin.register(OrderDelivery)
class OrderDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "delivery_date",
        "delivery_time",
        "delivery_status",
    )



@admin.register(EstimatedQuotation)
class EstimatedQuotationAdmin(admin.ModelAdmin):

    list_display = (
        "quotation",
        "base_total",
        "cgst_percent",
        "sgst_percent",
        "platform_fee_percent",
        "transport_charge",
        "final_total",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "quotation__id",
        "quotation__engineer__username",
        "quotation__agency__company_name",
    )

    readonly_fields = (
        "cgst_amount",
        "sgst_amount",
        "platform_fee_amount",
        "final_total",
        "created_at",
    )

from django.contrib import admin
from .models import FinalQuotationItem


@admin.register(FinalQuotationItem)
class FinalQuotationItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "final_estimate",
        "product_name",
        "quantity",
        "final_price",
        "get_total_price",
    )

    list_filter = ("final_estimate",)
    search_fields = ("product_name",)

    def get_total_price(self, obj):
        return obj.total_price()

    get_total_price.short_description = "Total Price"
