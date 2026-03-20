from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q,Sum,Count

from django.core.mail import send_mail
from django.conf import settings
# Create your views here.




def index(request):
    return render(request, 'index.html',{})

def home(request):
    return render(request, 'index.html',{})
def about(request):
    return render(request,'common/about.html',{})
def contact(request):
    return render(request,'common/contact.html',{})
def services(request):
    return render(request,'common/services.html',{})


# checkouts
def check_username(request):
    username = request.GET.get("username")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

def check_email(request):
    email = request.GET.get("email")
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})

def check_phone(request):
    phone = request.GET.get("phone")
    exists = Engineerprofile.objects.filter(phone_number=phone).exists()
    return JsonResponse({"exists": exists})

def check_username(request):
    username = request.GET.get("username")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

def check_email(request):
    email = request.GET.get("email")
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})



def check_company_phone(request):
    phone = request.GET.get("phone")
    exists = AgencyProfile.objects.filter(company_phone=phone).exists()
    return JsonResponse({"exists": exists})

def check_owner_phone(request):
    phone = request.GET.get("phone")
    exists = AgencyProfile.objects.filter(owner_phone=phone).exists()
    return JsonResponse({"exists": exists})


def check_gst(request):
    gst = request.GET.get("gst")
    exists = AgencyProfile.objects.filter(gst_number=gst).exists()
    return JsonResponse({"exists": exists})






# agency_side
def signup_agy(request):
    
    if request.method == "POST":

        old = request.POST   # 🔥 store old values ONLY for errors

        # ========== BASIC USER DETAILS ==========
        username = old.get("username")
        email = old.get("email")
        password = old.get("password")
        confirm_password = old.get("confirm_password")

        # ========== COMPANY DETAILS ==========
        company_name = old.get("company_name")
        gst_number = old.get("gst_number")
        confirm_gst = old.get("confirm_gst")
        gst_certificate = request.FILES.get("gst_certificate")

        company_phone = old.get("company_phone")
        company_address = old.get("company_address")
        company_district = old.get("company_district")
        company_state = old.get("company_state")
        company_pincode = old.get("company_pincode")

        # ========== OWNER DETAILS ==========
        owner_name = old.get("owner_name")
        owner_email = old.get("owner_email")
        owner_phone = old.get("owner_phone")
        gender = old.get("gender")
        owner_age = old.get("owner_age")
        owner_dob = old.get("owner_dob")
        owner_address = old.get("owner_address")
        owner_district = old.get("owner_district")
        owner_state = old.get("owner_state")
        owner_pincode = old.get("owner_pincode")

        # ========== TERMS ==========
        terms = old.get("terms_accepted")

        # ================= VALIDATIONS =================

        if not terms:
            messages.error(request, "Please accept terms and conditions")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if gst_number != confirm_gst:
            messages.error(request, "GST number does not match")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if int(owner_age) < 18:
            messages.error(request, "Owner age must be 18 or above")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        # ===== USER UNIQUE CHECK =====
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        # ===== AGENCY UNIQUE CHECK =====
        if AgencyProfile.objects.filter(company_phone=company_phone).exists():
            messages.error(request, "Company phone number already exists")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if AgencyProfile.objects.filter(owner_phone=owner_phone).exists():
            messages.error(request, "Owner phone number already exists")
            return render(request, "agency_side/agency_signup.html", {"old": old})

        if AgencyProfile.objects.filter(gst_number=gst_number).exists():
            messages.error(request, "GST number already registered")
            return render(request, "agency_side/agency_signup.html", {"old": old})
        
        

        # ================= CREATE USER + AGENCY PROFILE =================
        try:
            with transaction.atomic():

                # ----- CREATE USER -----
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                # ----- CREATE AGENCY PROFILE -----
                AgencyProfile.objects.create(
                    user=user,

                    company_name=company_name,
                    gst_number=gst_number,
                    gst_certificate=gst_certificate,
                    company_phone=company_phone,
                    company_address=company_address,
                    company_district=company_district,
                    company_state=company_state,
                    company_pincode=company_pincode,

                    owner_name=owner_name,
                    owner_email=owner_email,
                    owner_phone=owner_phone,
                    gender=gender,
                    owner_age=owner_age,
                    owner_dob=owner_dob,
                    owner_address=owner_address,
                    owner_district=owner_district,
                    owner_state=owner_state,
                    owner_pincode=owner_pincode,

                    terms_accepted=True
                )
                # 🔔 MAIL SEND
                # ----- SEND MAIL -----
                send_mail(
        "Welcome to ConstructWithUs – Your Agency Account is Ready",

        f"""
Dear {owner_name},

Welcome to ConstructWithUs!

🎉 Your agency account has been Created successfully on our platform.

Agency Details
----------------------------
Company Name : {company_name}
Username     : {username}

What you can do with your agency account:

• List and manage your construction materials.
• Receive quotation requests from engineers.
• Send quotations and generate final bills.
• Get confirmed orders directly from engineers.
• Expand your business by connecting with verified construction professionals.

You can now login to your agency dashboard and start adding your products.

If you need any assistance, feel free to contact our support team.

Thank you for choosing ConstructWithUs.

Best regards,  
ConstructWithUs Team

    
    """,

    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
             )

            messages.success(request, "Agency account created successfully. Please login.")
            return redirect("agy_login")   # 🔥 clears all inputs

        except Exception as e:
            print("AGENCY SIGNUP ERROR 👉", e)
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, "agency_side/agency_signup.html", {"old": old})

    # ========== GET REQUEST ==========
    return render(request, "agency_side/agency_signup.html")


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_agy(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # check agency role
            if hasattr(user, "agency_profile"):

                login(request, user)
                return redirect("agency_dash")

            else:
                messages.error(
    request,
    f'Invalid credentials to login as Agency user (Check It In Engineer Login). '
    f'<a href="{reverse("home")}" style="color:#0b1c2d; font-weight:600;">Go back</a>'
)
                return render(request, "agency_side/agency_login.html")

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "agency_side/agency_login.html")


def agency_logout(request):
    logout(request)
    return redirect("home")

#engineer_side
def engsignup(request):

    if request.method == "POST":

        old = request.POST   # 🔥 store old values ONLY for errors

        # ---------- BASIC DETAILS ----------
        username = old.get("username")
        email = old.get("email")
        password = old.get("password")
        confirm_password = old.get("confirmPassword")

        # ---------- EDUCATIONAL DETAILS ----------
        degree = old.get("degree")
        other_degree = old.get("other_degree")
        college = old.get("college")
        clg_district = old.get("clg_district")
        certificate = request.FILES.get("certificate")

        # ---------- PERSONAL DETAILS ----------
        fullname = old.get("fullname")
        age = old.get("age")
        gender = old.get("gender")
        dob = old.get("dob")
        phone = old.get("phone")
        address = old.get("address")
        engdistrict = old.get("district")
        state = old.get("state")
        pincode = old.get("pincode")

        # ---------- TERMS ----------
        terms = old.get("terms_accepted")

        # ================= VALIDATIONS =================

        if not terms:
            messages.error(request, "Please accept terms and conditions")
            return render(request, "engineer_side/eng_signup.html", {"old": old})

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "engineer_side/eng_signup.html", {"old": old})

        if int(age) < 18:
            messages.error(request, "Age must be 18 or above")
            return render(request, "engineer_side/eng_signup.html", {"old": old})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "engineer_side/eng_signup.html", {"old": old})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "engineer_side/eng_signup.html", {"old": old})

        if Engineerprofile.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists")
            return render(request, "engineer_side/eng_signup.html", {"old": old})
        
        

        # ================= CREATE USER + PROFILE =================
        try:
            with transaction.atomic():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                Engineerprofile.objects.create(
                    user=user,
                    email=email,
                    degree=degree,
                    other_degree=other_degree,
                    college_name=college,
                    clg_district=clg_district,
                    degree_certificate=certificate,
                    full_name=fullname,
                    age=age,
                    gender=gender,
                    date_of_birth=dob,
                    phone_number=phone,
                    address=address,
                    district=engdistrict,
                    state=state,
                    pincode=pincode,
                    terms_accepted=True
                )
                # 🔔 MAIL SEND
                send_mail(
"ConstructWithUs – Engineer Account Successfully Created",

f"""
Dear {fullname},

🎉Welcome to ConstructWithUs!

Your engineer account has been Created successfully.

Engineer Account Details
----------------------------
Name     : {fullname}
Username : {username}

With your ConstructWithUs engineer account, you can:

• 🏗️ Create and manage multiple construction sites.
• 📩 Request quotations for construction materials.
• 📩 Receive quotations from nearby verified suppliers.
• 💰 Compare prices and finalize the best quotation.
• 📦 Place orders directly with construction agencies.

Our platform helps engineers simplify material procurement and connect with trusted suppliers efficiently.

You can now login and start creating your project sites.
If you need any assistance, feel free to contact our support team.

Thank you for Joining ConstructWithUs.

Best regards,  
ConstructWithUs Team
""",

settings.EMAIL_HOST_USER,
[email],
fail_silently=False,
)

            messages.success(request, "Account created successfully. Please login.")
            return redirect("eng_login")   # 🔥 clears all inputs

        except Exception as e:
            print("ENGINEER SIGNUP ERROR 👉", e)
            messages.error(request, "Something went wrong. Please try again.")
        return render(request, "engineer_side/eng_signup.html", {"old": old})

    # ---------- GET REQUEST ----------
    return render(request, "engineer_side/eng_signup.html")

def englogin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # check engineer role safely
            if hasattr(user, "engineer_profile"):

                login(request, user)
                return redirect("eng_dash")

            else:
                messages.error(
    request,
    f'Invalid credentials to login as  Engineer user (Check It in Agency Login). '
    f'<a href="{reverse("home")}" style="color:#0b1c2d; font-weight:600;">Go back</a>'
)
                return render(request, "engineer_side/eng_login.html")

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "engineer_side/eng_login.html")



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AgencyProfile

@login_required
def agency_profile(request):
    agency = AgencyProfile.objects.get(user=request.user)

    if request.method == "POST":
        # only editable fields
        agency.company_phone = request.POST.get("company_phone")
        agency.owner_email = request.POST.get("owner_email")
        agency.company_address = request.POST.get("company_address")

        agency.save()
        messages.success(request, "Profile updated successfully")

        return redirect("agency_profile")

    return render(request, "agency_side/agency_profile.html", {
        "agency": agency
    })


def ag_dashboard(request):
    return render(request,'agency_side/agency_dashboard.html',{})

def ag_products(request):
    return render(request,'agency_side/my_products.html',{})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def all_products(request):

    products = Product.objects.filter(
        agency=request.user.agency_profile
    ).prefetch_related("variants").annotate(
    total_stock=Sum("variants__stock"),variant_count=Count("variants", filter=Q(variants__is_active=True))
)

    context = {
        "products": products,
        "active_tab": "all"
    }

    return render(request, "agency_side/all_products.html", context)

@login_required
def agency_all_products(request):

    agency = AgencyProfile.objects.get(user=request.user)
    category = request.GET.get("type", "all")
    

    if category != "all":
        products = Product.objects.filter(
            agency=agency,
            product_type=category
        )
    else:
        products = Product.objects.filter(agency=agency)

    return render(request, "agency_side/all_products.html", {
        "products": products,
        "active_type": category
    })

@login_required
def edit_delete_product(request):

    agency = AgencyProfile.objects.get(user=request.user)
    category = request.GET.get("type", "all")

    products = Product.objects.filter(agency=agency)

    if category != "all":
        products = products.filter(product_type=category)

    return render(request, "agency_side/edit_delete_product.html", {
        "products": products,
        "active_type": category
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, AgencyProfile
from django.utils import timezone


@login_required
def add_product(request):

    agency = AgencyProfile.objects.get(user=request.user)

    if request.method == "POST":

        product_type = request.POST.get("product_type")
        other_product_type = request.POST.get("other_product_type")
        brand_name = request.POST.get("brand_name")
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        # 🔥 Validate "Others"
        if product_type == "others" and not other_product_type:
            messages.error(request, "Please specify product type.")
            return redirect("add_product")

        Product.objects.create(
            agency=agency,
            product_type=product_type,
            other_product_type=other_product_type if product_type == "others" else None,
            brand_name=brand_name,
            product_name=product_name,
            description=description,
            image=image,
            address=agency.company_address,   # ✅ auto from agency
            pincode=agency.company_pincode,   # ✅ auto from agency
            created_at=timezone.localtime()
        )
        # 🔔 SEND EMAIL
        send_mail(
            "ConstructWithUs – Product Created Successfully",
            f"""
Dear {agency.owner_name},

Your product has been successfully created on ConstructWithUs.

Product Details
----------------------------
Agency Name  : {agency.company_name}
Brand Name   : {brand_name}
Product Name : {product_name}
Product Type : {product_type}

Your product has now been added to your agency catalog.

Next Step
----------------------------
You can now add product variants such as size, weight, price, and stock.

To do this, go to the "Add Product Variants" section and select the product name.

Adding variants will allow engineers to view available sizes and place material requests.

Thank you for using ConstructWithUs.

Best regards,  
ConstructWithUs Team
            """,
            settings.EMAIL_HOST_USER,
            [agency.user.email],
            fail_silently=False,
        )

        messages.success(request, "Product created successfully. Now add variations.")
        return redirect("add_product_variation")

    return render(request, "agency_side/add_product.html", {
        "active_tab": "add",
        "agency": agency
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, ProductVariants, AgencyProfile
from django.contrib import messages


from django.core.mail import send_mail
from django.conf import settings

@login_required
def add_product_variation(request):

    agency = AgencyProfile.objects.get(user=request.user)
    products = Product.objects.filter(agency=agency)

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        variant = ProductVariants.objects.create(
            product_id=product_id,
            spc_product_name=request.POST.get("spc_product_name"),
            size_or_weight=request.POST.get("size_or_weight"),
            unit=request.POST.get("unit"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock")
        )

        product = variant.product

        # 🔔 SEND EMAIL
        send_mail(
            "ConstructWithUs – Product Variant Added Successfully",
            f"""
Dear {agency.owner_name},

Your product variant has been successfully added on ConstructWithUs. 🎉

Product Information
----------------------------
Agency Name   : {agency.company_name}
Brand Name    : {product.brand_name}
Product Name  : {product.product_name}
Product Type  : {product.get_product_type_display()}

Variant Details
----------------------------
Variant Name  : {variant.spc_product_name}
Size / Weight : {variant.size_or_weight}
Unit          : {variant.unit}
Price         : ₹{variant.price}
Stock         : {variant.stock}

This variant is now visible to engineers searching for construction materials.

Engineers can now:
• View this product variant
• Check available stock
• Send quotation requests

You can manage or update your products anytime from your agency dashboard.

Thank you for growing your business with ConstructWithUs. 🚀

Best regards,  
ConstructWithUs Team
            """,
            settings.EMAIL_HOST_USER,
            [agency.user.email],
            fail_silently=False,
        )

        messages.success(request, "Product variation added successfully")
        return redirect("add_product_variation")

    variations = ProductVariants.objects.filter(product__agency=agency)

    return render(request, "agency_side/add_product_variations.html", {
        "products": products,
        "variations": variations,
        "active_tab": "variation"
    })

from django.core.mail import send_mail
from django.conf import settings

@login_required
def edit_product(request, product_id):

    agency = AgencyProfile.objects.get(user=request.user)

    product = get_object_or_404(
        Product,
        id=product_id,
        agency=agency
    )

    if request.method == "POST":

        product.brand_name = request.POST.get("brand_name")
        product.product_name = request.POST.get("product_name")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()

        variant_details = ""

        for variant in product.variants.all():

            variant.spc_product_name = request.POST.get(f"spc_name_{variant.id}")
            variant.size_or_weight = request.POST.get(f"size_{variant.id}")
            variant.unit = request.POST.get(f"unit_{variant.id}")
            variant.price = request.POST.get(f"price_{variant.id}")
            variant.stock = request.POST.get(f"stock_{variant.id}")
            variant.save()

            # collect variant details for mail
            variant_details += f"""
Variant Name  : {variant.spc_product_name}
Size / Weight : {variant.size_or_weight}
Unit          : {variant.unit}
Price         : ₹{variant.price}
Stock         : {variant.stock}
----------------------------------
"""

        # 🔔 SEND MAIL
        send_mail(
            "ConstructWithUs – Product Details Updated Successfully",
            f"""
Dear {agency.owner_name},

Your product details have been successfully updated on ConstructWithUs. ✏️

Product Information
----------------------------
Agency Name   : {agency.company_name}
Brand Name    : {product.brand_name}
Product Name  : {product.product_name}
Product Type  : {product.get_product_type_display()}

Updated Variant Details
----------------------------
{variant_details}

These updates are now visible to engineers searching for construction materials.

You can manage or update your products anytime from your agency dashboard.

Thank you for using ConstructWithUs to manage your construction material supply. 🚀

Best regards,  
ConstructWithUs Team
            """,
            settings.EMAIL_HOST_USER,
            [agency.user.email],
            fail_silently=False,
        )

        messages.success(request, "Product updated successfully")

        return redirect("agency_edit_product", product_id=product.id)

    return render(request, "agency_side/edit_product.html", {
        "product": product
    })


@login_required
def delete_product(request, product_id):

    agency = AgencyProfile.objects.get(user=request.user)

    product = get_object_or_404(
        Product,
        id=product_id,
        agency=agency
    )

    return render(request,
                  "agency_side/delete_product.html",
                  {"product": product})


from django.core.mail import send_mail
from django.conf import settings

@login_required
def delete_variant(request, variant_id):

    agency = AgencyProfile.objects.get(user=request.user)

    variant = get_object_or_404(
        ProductVariants,
        id=variant_id,
        product__agency=agency
    )

    product = variant.product
    product_id = product.id

    # 🔹 Store deleted variant details before delete
    deleted_variant_details = f"""
Deleted Variant
----------------------------
Variant Name  : {variant.spc_product_name}
Size / Weight : {variant.size_or_weight}
Unit          : {variant.unit}
Price         : ₹{variant.price}
Stock         : {variant.stock}
"""

    # 🔹 Delete variant
    variant.delete()

    # 🔹 Remaining variants
    remaining_variants = product.variants.all()

    remaining_text = ""
    if remaining_variants.exists():
        remaining_text = "\nRemaining Variants\n----------------------------\n"
        for v in remaining_variants:
            remaining_text += f"""
Variant Name  : {v.spc_product_name}
Size / Weight : {v.size_or_weight}
Unit          : {v.unit}
Price         : ₹{v.price}
Stock         : {v.stock}
----------------------------------
"""
    else:
        remaining_text = "\nNo variants remaining for this product.\n"

    # 🔔 SEND MAIL
    send_mail(
        "ConstructWithUs – Product Variant Deleted",
        f"""
Dear {agency.owner_name},

A product variant has been removed from your catalog on ConstructWithUs.

Product Information
----------------------------
Agency Name  : {agency.company_name}
Brand Name   : {product.brand_name}
Product Name : {product.product_name}
Product Type : {product.get_product_type_display()}

{deleted_variant_details}

{remaining_text}

You can add new variants or update product details anytime from your agency dashboard.

Thank you for managing your construction materials with ConstructWithUs.

Best regards,  
ConstructWithUs Team
        """,
        settings.EMAIL_HOST_USER,
        [agency.user.email],
        fail_silently=False,
    )

    messages.success(request, "Variant deleted successfully")

    return redirect("agency_delete_product", product_id=product_id)
    



from django.core.mail import send_mail
from django.conf import settings

@login_required
def delete_product_confirm(request, product_id):

    agency = AgencyProfile.objects.get(user=request.user)

    product = get_object_or_404(
        Product,
        id=product_id,
        agency=agency
    )

    # 🔹 store product details before delete
    product_details = f"""
Product Information
----------------------------
Agency Name  : {agency.company_name}
Brand Name   : {product.brand_name}
Product Name : {product.product_name}
Product Type : {product.get_product_type_display()}
"""

    # 🔹 collect variants
    variants = product.variants.all()

    variant_text = ""
    if variants.exists():
        variant_text = "\nVariants Deleted\n----------------------------\n"
        for v in variants:
            variant_text += f"""
Variant Name  : {v.spc_product_name}
Size / Weight : {v.size_or_weight}
Unit          : {v.unit}
Price         : ₹{v.price}
Stock         : {v.stock}
----------------------------------
"""
    else:
        variant_text = "\nNo variants were available for this product.\n"

    # 🔹 delete product
    product.delete()

    # 🔔 SEND MAIL
    send_mail(
        "ConstructWithUs – Product Deleted Successfully",
        f"""
Dear {agency.owner_name},

⚠ The Above product And Their Variants has been removed from your ConstructWithUs catalog.

{product_details}

{variant_text}

🗑 These product and variant records have been deleted successfully from your agency inventory.

You can add new products anytime from your agency dashboard.

Thank you for managing your construction materials with ConstructWithUs. 🚀

Best regards,  
ConstructWithUs Team
        """,
        settings.EMAIL_HOST_USER,
        [agency.user.email],
        fail_silently=False,
    )

    messages.success(request, "Product and related variants deleted successfully")

    return redirect("edit_delete_product")




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Engineerprofile

@login_required
def engineer_profile(request):

    profile = get_object_or_404(
        Engineerprofile,
        user=request.user
    )

    if request.method == "POST":

        profile.email = request.POST.get("email")
        profile.degree = request.POST.get("degree")
        profile.other_degree = request.POST.get("other_degree")
        profile.college_name = request.POST.get("college_name")
        profile.clg_district = request.POST.get("clg_district")

        if request.FILES.get("degree_certificate"):
            profile.degree_certificate = request.FILES.get("degree_certificate")

        profile.full_name = request.POST.get("full_name")
        profile.age = request.POST.get("age")
        profile.gender = request.POST.get("gender")
        profile.date_of_birth = request.POST.get("date_of_birth")
        profile.phone_number = request.POST.get("phone_number")
        profile.address = request.POST.get("address")
        profile.district = request.POST.get("district")
        profile.state = request.POST.get("state")
        profile.pincode = request.POST.get("pincode")

        profile.save()

        messages.success(request, "Profile updated successfully ✅")

        return redirect("eng_profile")

    return render(request, "engineer_side/engineer_profile.html", {
        "profile": profile,
        "degree_choices": Engineerprofile.DEGREE_CHOICES
    })

from datetime import datetime
#agency_side

def eng_dashboard(request):
    return render(request,'engineer_side/engineer_dashboard.html',{})


def engineer_logout(request):
    logout(request)
    return redirect("home")   # or engineer_login


@login_required
def create_site(request):

    if request.method == "POST":

        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        total_sqft=request.POST.get("total_sqft")
        building_area_sqft=request.POST.get("building_area_sqft")



        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        today = timezone.now().date()

        try:
            total_sqft = float(request.POST.get("total_sqft", 0))
            building_area_sqft = float(request.POST.get("building_area_sqft", 0))
        except ValueError:
            messages.error(request, "Invalid Sqft value ❌")
            return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST,
        "today": timezone.now().date()
    })


        # 🚫 Past date check
        if start_date < today:
            messages.error(request, "Start date cannot be in the past ❌")
            return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST
    })

        if end_date < today:
            messages.error(request, "End date cannot be in the past ❌")
            return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST
    })

        if end_date <= start_date:
            messages.error(
                request,
                "End date must be greater than Start date ❌"
            )
            return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST
    })
        
        if building_area_sqft > total_sqft:
            messages.error(request, "Building Sqft cannot be greater than Total Sqft ❌")
            return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST,
        "today": timezone.now().date()
    })


        # ✅ DEFINE THESE BEFORE USING
        category = request.POST.get("category")
        other_category = request.POST.get("other_category")

        site = ConstructionSite.objects.create(
            engineer=request.user,
            site_name=request.POST.get("site_name"),
            category=category,
            other_category=other_category if category == "others" else None,
            total_sqft=request.POST.get("total_sqft"),
            building_area_sqft=request.POST.get("building_area_sqft"),
            approximate_budget=request.POST.get("approximate_budget"),
            start_date=start_date,   # use converted date
            end_date=end_date,       # use converted date
            site_address=request.POST.get("site_address"),
            site_district=request.POST.get("site_district"),
            site_state=request.POST.get("site_state"),
            site_pincode=request.POST.get("site_pincode"),
            site_map=request.FILES.get("site_map"),
            blueprint_file=request.FILES.get("blueprint_file"),
        )

        SiteOwner.objects.create(
            site=site,
            owner_name=request.POST.get("owner_name"),
            owner_gender=request.POST.get("owner_gender"),
            owner_phone=request.POST.get("owner_phone"),
            owner_address=request.POST.get("owner_address"),
            owner_district=request.POST.get("owner_district"),
            owner_pincode=request.POST.get("owner_pincode"),
        )
        # 🔔 SEND MAIL - Site Created Notification

        engineer_name = request.user.engineer_profile.full_name
        email = request.user.email

        subject = f"🏗️ ConstructWithUs – Site Created Successfully ({site.site_name})"

        message = f"""
Hello {engineer_name},

🎉 Your construction site has been successfully created on ConstructWithUs.

        Site Details
        ----------------------------
        Site Name : {site.site_name}
        Status : {site.status}
        Address :{site.site_address}
        District  : {site.site_district}
        Start Date: {site.start_date}

You can now start managing your construction project with ease.

What you can do next:

• 🏗️ Add construction materials to your cart
• 📩 Request quotations from verified suppliers
• 💰 Compare prices and choose the best offer
• 📦 Place orders directly from trusted agencies
• 📊 Track all orders and project materials

ConstructWithUs helps you simplify construction material procurement.

Thank you for using ConstructWithUs.

Best regards,
ConstructWithUs Team
"""

        send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)

        messages.success(
            request,
            "Site created successfully ✅ Check it in All Sites tab."
        )

        return redirect("create_site")

    return render(request, "engineer_side/site_creation.html", {
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "active_tab": "create",
        "form_data": request.POST,
        "today": timezone.now().date()
    })


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ConstructionSite

@login_required
def all_sites(request):

    query = request.GET.get("q")

    sites = ConstructionSite.objects.filter(
        engineer=request.user
    ).order_by("-created_at")

    if query:
        sites = sites.filter(
            Q(site_name__icontains=query) |
            Q(status__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "engineer_side/all_sites.html", {
        "sites": sites,
        "active_tab": "all",
        "query": query
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ConstructionSite

@login_required
def site_details(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    return render(request, "engineer_side/site_details.html", {
        "site": site
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ConstructionSite

@login_required
def edit_delete_site(request):

    sites = ConstructionSite.objects.filter(
        engineer=request.user
    ).select_related("owner").order_by("-created_at")
    return render(request,
        "engineer_side/edit_delete_sites.html",
        {
            "sites": sites,
            "active_tab": "edit"
        }
    )

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConstructionSite, SiteOwner

@login_required
def edit_site_details(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    owner = get_object_or_404(SiteOwner, site=site)

    if request.method == "POST":

        # ===== UPDATE SITE =====
        site.site_name = request.POST.get("site_name")
        site.category = request.POST.get("category")
        site.other_category = request.POST.get("other_category")
        site.total_sqft = request.POST.get("total_sqft")
        site.building_area_sqft = request.POST.get("building_area_sqft")
        site.approximate_budget = request.POST.get("approximate_budget")
        site.start_date = request.POST.get("start_date")
        site.end_date = request.POST.get("end_date")
        site.status = request.POST.get("status")
        site.description = request.POST.get("description")
        site.site_address = request.POST.get("site_address")
        site.site_district = request.POST.get("site_district")
        site.site_state = request.POST.get("site_state")
        site.site_pincode = request.POST.get("site_pincode")

        if request.FILES.get("site_map"):
            site.site_map = request.FILES.get("site_map")

        if request.FILES.get("blueprint_file"):
            site.blueprint_file = request.FILES.get("blueprint_file")

        site.save()

        # ===== UPDATE OWNER =====
        owner.owner_name = request.POST.get("owner_name")
        owner.owner_gender = request.POST.get("owner_gender")
        owner.owner_phone = request.POST.get("owner_phone")
        owner.owner_address = request.POST.get("owner_address")
        owner.owner_district = request.POST.get("owner_district")
        owner.owner_pincode = request.POST.get("owner_pincode")

        owner.save()

         # 🔔 SEND MAIL - Site Created Notification

        engineer_name = request.user.engineer_profile.full_name
        email = request.user.email

        subject = f"🏗️ ConstructWithUs – Site Nmae:({site.site_name}) and Site owner details updated Successfully"

        message = f"""
Hello {engineer_name},

🎉 Your construction Site and owner details updated.

        Site Details
        ----------------------------
        Site Name : {site.site_name}
        Status : {site.status}

Check it out ,inside your dashboard !!            

Thank you for using ConstructWithUs.

Best regards,
ConstructWithUs Team
"""

        send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)

        

        messages.success(request, "Site updated successfully ✅")
        return redirect("edit_site_details", site_id=site.id)

    return render(request, "engineer_side/edit_sites.html", {
        "site": site,
        "owner": owner,
        "category_choices": ConstructionSite.SITE_CATEGORY_CHOICES,
        "status_choices": ConstructionSite.STATUS_CHOICES
    })

@login_required
def delete_site(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )
    
    owner = site.owner

    if request.method == "POST":
        site_name = site.site_name
        site.delete()   # Owner auto deletes (CASCADE)

        # 🔔 send mail
        engineer_name = request.user.engineer_profile.full_name
        email = request.user.email

        subject = f"⚠️ ConstructWithUs – Your Site Name:({site.site_name}) Deleted Successfully"

        message = f"""
Hello {engineer_name},

Your construction site has been removed from ConstructWithUs.

Deleted Site Details
----------------------------
Site Name : {site_name}

You can still create and manage new construction sites anytime.

If this action was done by mistake, you can create the site again from your dashboard.

Thank you for using ConstructWithUs.

Best regards,
ConstructWithUs Team
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Site and Owner details deleted successfully."
        )

        return redirect("edit_delete_site")

    return render(
        request,
        "engineer_side/delete_site.html",
        {
            "site": site,
            "owner": owner
        }
    )

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConstructionSite


@login_required
def manage_site_construction_materials(request, site_id):

    # 🔒 Ensure engineer accessing only their own site
    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    context = {
        "site": site,
        "active_tab": "materials"
    }

    return render(
        request,
        "engineer_side/manage_site_construction_materials.html",
        context
    )

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
@login_required
def search_products(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    agencies = AgencyProfile.objects.filter(
        company_district__iexact=site.site_district
    ).prefetch_related("products")

    # GET params
    query = request.GET.get("q", "").strip()
    pincode = request.GET.get("pincode", site.site_pincode)
    product_type = request.GET.get("type", "all")
    agency_name = request.GET.get("agency")

    # Base queryset
    products = Product.objects.filter(
        pincode=pincode
    ).prefetch_related("variants").annotate(
        total_stock=Sum("variants__stock"),
        variant_count=Count("variants", filter=Q(variants__is_active=True))
    )

    # 🔹 Agency filter
    if agency_name:
        products = products.filter(
            agency__company_name__icontains=agency_name
        )

    # 🔹 Search filter
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(agency__company_name__icontains=query)
        )

    # 🔹 Product type filter
    if product_type != "all":
        products = products.filter(product_type=product_type)

    products = products.order_by("-created_at")

    context = {
        "site": site,
        "products": products,
        "query": query,
        "pincode": pincode,
        "active_tab": "search",
        "agencies": agencies,
        "agency_name": agency_name,
        "active_type": product_type,
    }

    return render(
        request,
        "engineer_side/search_products.html",
        context
    )


@login_required
def add_to_cart(request, site_id, variant_id):

    if request.method == "POST":

        site = get_object_or_404(
            ConstructionSite,
            id=site_id,
            engineer=request.user
        )

        variant = get_object_or_404(ProductVariants, id=variant_id)

        quantity = int(request.POST.get("quantity", 1))

        CartItem.objects.create(
            site=site,
            product=variant.product,
            variant=variant,
            product_name=variant.product.product_name,
            weight_or_size=variant.size_or_weight,
            average_price=variant.price,
            quantity=quantity
        )
        # ✅ success message
        messages.success(
            request,
            f"product Name :{variant.product.product_name} added to cart successfully."
        )

    return redirect("search_products", site_id=site.id)

@login_required
def remove_cart_item(request, site_id, item_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        site=site
    )

    cart_item.delete()
    messages.success(
            request,
            f"product Removed From cart successfully."
        )

    return redirect("view_cart", site_id=site.id)


@login_required
def view_cart(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    cart_items = site.cart_items.all().order_by("product__agency__company_name","-created_at")

    total_amount = sum(item.total_price for item in cart_items)

    context = {
        "site": site,
        "cart_items": cart_items,
        "active_tab": "cart",
        "total_amount": total_amount,
    }

    return render(
        request,
        "engineer_side/add_to_cart.html",
        context
    )

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

@login_required
def request_quotation(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    engineer_name = request.user.get_full_name() or request.user.username

    if request.method == "POST":

        delivery_pref = request.POST.get("delivery_preference")
        expected_date = request.POST.get("expected_date")

        item_id = request.POST.get("item_id")
        agency_id = request.POST.get("agency_id")

        quotation = None
        agency = None

        # ---------------- SINGLE PRODUCT ----------------

        if item_id:

            cart_item = get_object_or_404(
                CartItem,
                id=item_id,
                site=site
            )

            agency = cart_item.product.agency

            quotation = QuotationRequest.objects.create(
                site=site,
                engineer=request.user,
                agency=agency,
                delivery_preference=delivery_pref,
                expected_delivery_date=expected_date,
                request_note="Single product quotation request",
                estimated_total=cart_item.total_price
            )

            QuotationItem.objects.create(
                quotation=quotation,
                product_name=cart_item.product_name,
                weight_or_size=cart_item.weight_or_size,
                quantity=cart_item.quantity,
                price=cart_item.average_price
            )

            cart_item.delete()

        # ---------------- AGENCY PRODUCTS ----------------

        elif agency_id:

            cart_items = site.cart_items.filter(
                product__agency_id=agency_id
            )

            if not cart_items.exists():
                return redirect("view_cart", site_id=site.id)

            agency = cart_items.first().product.agency

            total_amount = sum(item.total_price for item in cart_items)

            quotation = QuotationRequest.objects.create(
                site=site,
                engineer=request.user,
                agency=agency,
                delivery_preference=delivery_pref,
                expected_delivery_date=expected_date,
                request_note="Agency quotation request",
                estimated_total=total_amount
            )

            for item in cart_items:
                QuotationItem.objects.create(
                    quotation=quotation,
                    product_name=item.product_name,
                    weight_or_size=item.weight_or_size,
                    quantity=item.quantity,
                    price=item.average_price
                )

            cart_items.delete()

        # ---------------- EMAIL SECTION ----------------

        engineer_email = request.user.email
        agency_email = agency.user.email

        # product details for mail
        product_details = ""

        for item in quotation.items.all():
            product_details += f"""
Product : {item.product_name}
Size : {item.weight_or_size}
Quantity : {item.quantity}
Unit Price : ₹{item.price}
Total : ₹{item.total_price()}
-----------------------------
"""

        current_time = timezone.localtime().strftime("%d %B %Y, %I:%M %p")

        # -------- engineer mail --------

        engineer_message = f"""
Hello {engineer_name},

Your quotation request has been successfully sent to Agency:{agency.company_name}

Quotation ID : #{quotation.id}
Agency : {agency.company_name}

Requested On : {current_time}

Delivery Preference : {quotation.delivery_preference}
Expected Delivery Date : {quotation.expected_delivery_date}

Requested Products
-----------------------------
{product_details}

Estimated Total Amount : ₹{quotation.estimated_total}

You will receive a reply once the agency reviews your request.

ConstructWithUs Team
"""

        send_mail(
            f"Quotation Request Sent (ID #{quotation.id})",
            engineer_message,
            settings.EMAIL_HOST_USER,
            [engineer_email],
            fail_silently=True
        )

        # -------- agency mail --------

        agency_message = f"""
Hello {agency.company_name},

You received a new quotation request.

Quotation ID : #{quotation.id}

Engineer : {request.user.get_full_name()}
Site : {site.site_name}

Requested On : {current_time}

Delivery Preference : {quotation.delivery_preference}
Expected Delivery Date : {quotation.expected_delivery_date}

Requested Products
-----------------------------
{product_details}

Estimated Total Amount : ₹{quotation.estimated_total}

Login to your dashboard to reply.

ConstructWithUs Platform
"""

        send_mail(
            f"New Quotation Request Received (ID #{quotation.id})",
            agency_message,
            settings.EMAIL_HOST_USER,
            [agency_email],
            fail_silently=True
        )

        # success message

        messages.success(
            request,
            f"Quotation request #{quotation.id} sent successfully to {agency.company_name}"
        )

        return redirect("view_quotation_invoice", quotation.id)
    

#agency kaga
@login_required
def agency_show_final_bill(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        agency=request.user.agency_profile   # 🔥 important
    )

    final_estimate = get_object_or_404(
        EstimatedQuotation,
        quotation=quotation
    )

    return render(
        request,
        "agency_side/show_final_bill.html",
        {
            "quotation": quotation,
            "final_estimate": final_estimate
        }
    )

@login_required
def view_quotation_invoice(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id
    )

    items = quotation.items.all()

    return render(
        request,
        "engineer_side/request_quotation.html",
        {
            "quotation": quotation,
            "items": items,
            "site": quotation.site,
            "total_amount": quotation.estimated_total,
            "agency": quotation.agency,
            "engineer": quotation.engineer,
        }
    )



@login_required
def manage_requested_replies(request):

    agency = request.user.agency_profile

    # 🔹 Incoming requests
    incoming_requests = QuotationRequest.objects.filter(
        agency=agency
    ).filter(
        Q(status="Requested") |
        Q(status="Approved", final_estimate__isnull=True)
    ).order_by("-created_at")


    # 🔹 Replied quotations
    replied_requests = QuotationRequest.objects.filter(
        agency=agency
    ).filter(
        Q(status="Rejected") |
        Q(status="Approved", final_estimate__isnull=False)
    ).order_by("-created_at")


    context = {
        "incoming_requests": incoming_requests,
        "replied_requests": replied_requests,
    }

    return render(
        request,
        "agency_side/manage_requested_replies.html",
        context
    )


@login_required
def products_quotation_page(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        
    )
    return render(
        request,
        "agency_side/products_quotation_page.html",
        {
            "quotation": quotation
        }
    )

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages


@login_required
def update_quotation_status(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in ["Approved", "Rejected"]:

            quotation.status = new_status
            quotation.save()

            agency = quotation.agency
            engineer = quotation.engineer

            engineer_email = engineer.email
            agency_email = agency.user.email

            update_time = timezone.localtime().strftime("%d %B %Y, %I:%M %p")

            # ---------------- Engineer Mail ----------------

            engineer_message = f"""
Hello {engineer.get_full_name() or engineer.username},

Your quotation request status has been updated.

Quotation ID : #{quotation.id}
Agency : {agency.company_name}
Site : {quotation.site.site_name}

Status : {new_status}

Updated On :
{update_time}

Please login to your dashboard to view the details.

ConstructWithUs Team
"""

            send_mail(
                f"Quotation Status Updated (ID #{quotation.id})",
                engineer_message,
                settings.EMAIL_HOST_USER,
                [engineer_email],
                fail_silently=True
            )

            # ---------------- Agency Confirmation Mail ----------------

            agency_message = f"""
Hello {agency.company_name},

You successfully updated a quotation request reply ,succesfully sended to engineer {engineer.get_full_name() or engineer.username}

Quotation ID : #{quotation.id}
Site : {quotation.site.site_name}

New Status : {new_status}

Updated On :
{update_time}

Thank you for responding to the quotation request.

ConstructWithUs Platform
"""

            send_mail(
                f"Quotation #{quotation.id} Status Updated Successfully",
                agency_message,
                settings.EMAIL_HOST_USER,
                [agency_email],
                fail_silently=True
            )

            messages.success(
                request,
                f"Quotation #{quotation.id} status updated to {new_status}"
            )

    return redirect("manage_requested_replies")


from decimal import Decimal

#agency_side
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

@login_required
def generate_final_bill(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        agency=request.user.agency_profile
    )
    

    if request.method == "POST":
        print("POST DATA:", request.POST)
        base_total = Decimal("0.00")
        product_details = ""

        # 1️⃣ Calculate base total
        for item in quotation.items.all():

            edited_price = request.POST.get(f"final_price_{item.id}")

            if edited_price:
                edited_price = Decimal(edited_price)
            else:
                edited_price = item.price

            line_total = edited_price * item.quantity
            base_total += line_total

            product_details += f"""
Product : {item.product_name}
Size : {item.weight_or_size}
Quantity : {item.quantity}
Final Price : ₹{edited_price}
Total : ₹{line_total}
-----------------------------
"""

        # 2️⃣ Tax inputs
        cgst_percent = Decimal(request.POST.get("cgst_percent", "0"))
        sgst_percent = Decimal(request.POST.get("sgst_percent", "0"))
        platform_percent = Decimal(request.POST.get("platform_fee_percent", "0"))
        transport = Decimal(request.POST.get("transport_charge", "0"))

        # 3️⃣ Calculate tax
        cgst_amount = (base_total * cgst_percent) / Decimal("100")
        sgst_amount = (base_total * sgst_percent) / Decimal("100")
        platform_amount = (base_total * platform_percent) / Decimal("100")

        final_total = (
            base_total +
            cgst_amount +
            sgst_amount +
            platform_amount +
            transport
        )

        # 4️⃣ Save EstimatedQuotation
        estimate, created = EstimatedQuotation.objects.update_or_create(
            quotation=quotation,
            defaults={
                "base_total": base_total,
                "transport_charge": transport,
                "cgst_percent": cgst_percent,
                "sgst_percent": sgst_percent,
                "platform_fee_percent": platform_percent,
                "cgst_amount": cgst_amount,
                "sgst_amount": sgst_amount,
                "platform_fee_amount": platform_amount,
                "final_total": final_total,
            }
        )

        # 5️⃣ Delete old items
        estimate.final_items.all().delete()

        # 6️⃣ Save FinalQuotationItem
        for item in quotation.items.all():

            edited_price = request.POST.get(f"final_price_{item.id}")

            if edited_price:
                edited_price = Decimal(edited_price)
            else:
                edited_price = item.price

            FinalQuotationItem.objects.create(
                final_estimate=estimate,
                product_name=item.product_name,
                weight_or_size=item.weight_or_size,
                quantity=item.quantity,
                final_price=edited_price
            )
        
        
        quotation.status = "Approved"
        quotation.save()

        # ===============================
        # EMAIL SECTION
        # ===============================

        engineer = quotation.engineer
        agency = quotation.agency

        engineer_email = engineer.email
        agency_email = agency.user.email

        # Engineer mail
        send_mail(
            f"Final Quotation #{quotation.id} Ready",
            f"""
Hello Engineer {engineer.get_full_name() or engineer.username},

Your quotation request #{quotation.id} has been finalized by {agency.company_name}.

This Generated bill Valid Until :  Today 8:00pm

Final Product Prices
-----------------------------
{product_details}

Final Total Amount : ₹{final_total}

If you are okay with this price,
please place your order before the quotation expiry time.

If you are not satisfied with the price, After the quotation expired today 8:00pm
you can request a regenerated quotation for next day pricing.

Thank you for using ConstructWithUs.

ConstructWithUs Team
""",
            settings.EMAIL_HOST_USER,
            [engineer_email],
            fail_silently=False
        )

        # Agency mail
        send_mail(
            f"Final Quotation Sent to Engineer #{quotation.id}",
            f"""
Hello {agency.company_name},

You have successfully sent the final quotation to the engineer.

Quotation ID : #{quotation.id}

This Generated bill Valid Until : Today 8:00pm

Product Details
-----------------------------
{product_details}

Final Total : ₹{final_total}

If the engineer accepts the price,
they will place the order before quotation expiry.

ConstructWithUs Platform
""",
            settings.EMAIL_HOST_USER,
            [agency_email],
            fail_silently=False
        )

        return redirect("manage_requested_replies")

    return render(
        request,
        "agency_side/generate_final_bill.html",
        {"quotation": quotation}
    )


@login_required
def regenerate_quotation_bill(request, quotation_id):

    old = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        engineer=request.user
    )

    if request.method == "POST":

        delivery_pref = request.POST.get("delivery_preference")
        expected_date = request.POST.get("expected_date")

        # create new quotation
        new_quotation = QuotationRequest.objects.create(
            site = old.site,
            engineer = old.engineer,
            agency = old.agency,
            delivery_preference = delivery_pref,
            expected_delivery_date = expected_date,
            estimated_total = old.estimated_total,
            request_note = "Regenerated quotation request"
        )

        # copy products
        product_details = ""

        for item in old.items.all():

            QuotationItem.objects.create(
                quotation = new_quotation,
                product_name = item.product_name,
                weight_or_size = item.weight_or_size,
                quantity = item.quantity,
                price = item.price
            )

            product_details += f"""
Product : {item.product_name}
Size : {item.weight_or_size}
Quantity : {item.quantity}
Unit Price : ₹{item.price}
-------------------------
"""

        # expire old quotation
        old.status = "Expired"
        old.save()

        engineer_email = request.user.email
        agency_email = old.agency.user.email

        # engineer mail
        send_mail(
            f"New Quotation Request Sent (ID #{new_quotation.id})",
            f"""
Hello {request.user.get_full_name()},

Your regenerated quotation request has been sent successfully to
{old.agency.company_name}.

New Quotation ID : #{new_quotation.id}

Requested Products
-------------------------
{product_details}

The agency will review your request and send updated pricing.

Please wait for the reply during official working hours.

Thank you for using ConstructWithUs.

ConstructWithUs Team
""",
            settings.EMAIL_HOST_USER,
            [engineer_email],
            fail_silently=True
        )

        # agency mail
        send_mail(
            f"Regenerated Quotation Request #{new_quotation.id}",
            f"""
Hello {old.agency.company_name},

Engineer {request.user.get_full_name()} has requested a regenerated quotation.

Quotation ID : #{new_quotation.id}

Delivery Preference : {delivery_pref}
Expected Delivery Date : {expected_date}

Requested Products
-------------------------
{product_details}

Please review the product list and provide updated pricing.

Kindly respond during official working hours
(Tomorrow after 9:00 AM).

Thank you for using ConstructWithUs.

ConstructWithUs Platform
""",
            settings.EMAIL_HOST_USER,
            [agency_email],
            fail_silently=True
        )

        messages.success(
            request,
            f"New quotation request #{new_quotation.id} sent successfully."
        )

        return redirect("view_quotation_invoice", new_quotation.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import QuotationRequest, EstimatedQuotation ,AgencyProfile


@login_required
def final_view_bill(request, quotation_id):

    # 1️⃣ Get quotation only if belongs to this engineer
    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        
    )

    # 2️⃣ Check final bill exists
    final_estimate = get_object_or_404(
        EstimatedQuotation,
        quotation=quotation
    )

    return render(
        request,
        "engineer_side/final_view_bill.html",
        {
            "quotation": quotation,
            "final_estimate": final_estimate,
        }
    )



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import QuotationRequest, EstimatedQuotation

@login_required
def place_order(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        engineer=request.user
    )

    final_estimate = quotation.final_estimate

    if request.method == "POST":

        # 🔹 Save delivery data in session
        delivery_date = request.POST.get("delivery_date")
        delivery_time = request.POST.get("delivery_time")

        if not delivery_date or not delivery_time:
            return redirect("place_order", quotation_id=quotation.id)

        request.session["delivery_date"] = delivery_date
        request.session["delivery_time"] = delivery_time

        
        return redirect("payment_page", quotation_id=quotation.id)

    return render(
        request,
        "engineer_side/place_order.html",
        {
            "quotation": quotation,
            "final_estimate": final_estimate
        }
    )


@login_required
def payment_page(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        engineer=request.user
    )

    final_estimate = quotation.final_estimate

    return render(request,
        "engineer_side/payment_page.html",
        {
            "quotation": quotation,
            "final_estimate": final_estimate
        }
    )


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (
    Order,
    OrderItem,
    OrderDelivery,
    EstimatedQuotation,
    QuotationRequest
)

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Order,
    OrderItem,
    OrderDelivery,
    EstimatedQuotation,
    QuotationRequest
)

@login_required
def confirm_cod_order(request, quotation_id):

    quotation = get_object_or_404(
        QuotationRequest,
        id=quotation_id,
        engineer=request.user
    )

    final_estimate = get_object_or_404(
        EstimatedQuotation,
        quotation=quotation
    )

    # Prevent duplicate order
    if Order.objects.filter(quotation=quotation).exists():
        return redirect("manage_quotations_orders", quotation.site.id)

    # 1️⃣ Create Order
    order = Order.objects.create(
        quotation=quotation,
        engineer=request.user,
        agency=quotation.agency,
        total_amount=final_estimate.final_total,
        payment_method="COD",
        cod_confirmed=True,
        cod_confirmed_at=timezone.now(),
        order_status="Placed"
    )

    product_details = ""

    # 2️⃣ Create Order Items
    for item in quotation.items.all():

        OrderItem.objects.create(
            order=order,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price()
        )

        product_details += f"""
Product : {item.product_name}
Quantity : {item.quantity}
Price : ₹{item.price}
-----------------------------
"""

    # 3️⃣ Delivery details
    delivery_date = request.session.get("delivery_date")
    delivery_time = request.session.get("delivery_time")

    if not delivery_date or not delivery_time:
        return redirect("place_order", quotation_id=quotation.id)

    OrderDelivery.objects.create(
        order=order,
        delivery_date=delivery_date,
        delivery_time=delivery_time,
        engineer_name=quotation.engineer.engineer_profile.full_name,
        engineer_phone=quotation.engineer.engineer_profile.phone_number,
        site_owner_phone=quotation.site.owner.owner_phone,
        site_address=quotation.site.site_address,
        site_district=quotation.site.site_district,
        site_pincode=quotation.site.site_pincode,
        delivery_status="Pending"
    )

    quotation.status = "MOVED_For_Order"
    quotation.save()

    # =============================
    # EMAIL SECTION
    # =============================

    engineer_email = quotation.engineer.email
    agency_email = quotation.agency.user.email

    # Engineer Mail
    send_mail(
    f"Order #{order.id} Placed Successfully",
    f"""
Hello {quotation.engineer.engineer_profile.full_name},

Your order has been placed successfully.

Order ID : #{order.id}
Order Time : {timezone.now()}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time} (24 hours Format)

Payment Method : {order.payment_method}
Products Ordered
-----------------------------
{product_details}

After all taxes and deliver charges

Total Amount : ₹{final_estimate.final_total}

Your order request has been sent to the agency.
They will review the order and update the status shortly.

You will receive updates once the agency approves or rejects the order.
You can track the order status from your dashboard.

Thank you for using ConstructWithUs.

ConstructWithUs Team
""",
    settings.EMAIL_HOST_USER,
    [engineer_email],
    fail_silently=False
)

    # Agency Mail
    send_mail(
    f"New Order Received #{order.id}",
    f"""
Hello {quotation.agency.company_name},

A new order has been received from the engineer.

Check it in Received orders section..

Order ID : #{order.id}
Engineer : {quotation.engineer.engineer_profile.full_name}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time} (24 hours Format)

Payment Method : {order.payment_method}
Products Ordered
-----------------------------
{product_details}

After all taxes and deliver charges

Total Order Amount : ₹{final_estimate.final_total}

Current Order Status : Placed

Please review the order and update the status as:

• Agency Approved
• Agency Rejected

After approval, you can proceed with delivery arrangements.

ConstructWithUs Platform
""",
    settings.EMAIL_HOST_USER,
    [agency_email],
    fail_silently=False
)
    messages.success(
    request,
    f"Order #{order.id} placed successfully. The agency will review your order shortly."
)

    return redirect("order_success_page", site_id=quotation.site.id)


@login_required
def order_success_page(request, site_id):
    return render(request, "engineer_side/order_placed_success.html", {
        "site_id": site_id
    })


# agency side 
@login_required
def manage_quotations_orders(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    # All quotations
    quotations = QuotationRequest.objects.filter(
        site=site
    ).order_by("-created_at")

    # Replied quotations only
    replied_quotations = QuotationRequest.objects.filter(
    engineer=request.user,
    status__in=["Approved", "Expired"]
).order_by("-created_at")

    return render(
        request,
        "engineer_side/manage_quotations_orders.html",
        {
            "site": site,
            "quotations": quotations,
            "replied_quotations": replied_quotations,
            "active_tab": "quotation"
        }
    )

#agency side
@login_required
def confirmed_orders(request, site_id):

    site = get_object_or_404(
        ConstructionSite,
        id=site_id,
        engineer=request.user
    )

    orders = Order.objects.filter(
        quotation__site=site,
        order_status__in=[
            "Placed",
            "AgencyApproved",
            "AgencyRejected",
            "Processing",
            "OutForDelivery",
            "Delivered",
            "Cancelled",
        ]
    ).select_related("quotation", "delivery").order_by("-created_at")

    return render(
        request,
        "engineer_side/confirmed_orders.html",
        {
            "site": site,
            "active_tab": "orders",
            "orders": orders
        }
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Order, EstimatedQuotation
@login_required
def agency_order_bill(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        agency=request.user.agency_profile
    )

    final_estimate = get_object_or_404(
        EstimatedQuotation,
        quotation=order.quotation
    )

    return render(
        request,
        "agency_side/agency_order_bill.html",
        {
            "order": order,
            "final_estimate": final_estimate
        }
    )


@login_required
def eng_order_bill(request, order_id):

    # 🔹 Ensure order belongs to this engineer
    order = get_object_or_404(
        Order,
        id=order_id,
        engineer=request.user
    )

    # 🔹 Get final estimate linked to quotation
    final_estimate = get_object_or_404(
        EstimatedQuotation,
        quotation=order.quotation
    )

    return render(
        request,
        "engineer_side/engineer_order_bill.html",
        {
            "order": order,
            "final_estimate": final_estimate
        }
    )


@login_required
def agency_orders(request):

    # Agency user check
    if not hasattr(request.user, "agency_profile"):
        return redirect("agency_login")

    agency = request.user.agency_profile

    orders = (
        Order.objects
        .filter(agency=agency)
        .select_related(
            "engineer",
            "quotation__site",
            "delivery"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "agency_side/agency_orders.html",
        {
            "orders": orders,
            "active_tab": "orders"
        }
    )



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


@login_required
def agency_update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        agency=request.user.agency_profile
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in ["AgencyApproved", "AgencyRejected"]:

            order.order_status = new_status
            order.save()

            # delivery details
            delivery = order.delivery

            delivery_date = delivery.delivery_date
            delivery_time = delivery.delivery_time

            # product list
            product_details = ""
            for item in order.items.all():

                product_details += f"""
Product : {item.product_name}
Quantity : {item.quantity}
Price : ₹{item.price}
-------------------------
"""

            engineer_email = order.engineer.email
            agency_email = order.agency.user.email

            status_text = "Approved" if new_status == "AgencyApproved" else "Rejected"

            # ==========================
            # Engineer Mail
            # ==========================

            send_mail(
                f"Order #{order.id} {status_text} by Agency",
                f"""
Hello {order.engineer.engineer_profile.full_name},

Your order has been reviewed by the agency.

Order ID : #{order.id}
Status Updated : {status_text}

Payment Method : {order.payment_method}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time}

Products Ordered
-------------------------
{product_details}

The agency has updated the order status.

You will receive further updates once the order is dispatched.

Thank you for using ConstructWithUs.

ConstructWithUs Team
""",
                settings.EMAIL_HOST_USER,
                [engineer_email],
                fail_silently=False
            )

            # ==========================
            # Agency Mail
            # ==========================

            send_mail(
                f"Order #{order.id} Status Updated ({status_text})",
                f"""
Hello {order.agency.company_name},

Order status has been updated successfully.

Order ID : #{order.id}
Status : {status_text}

Payment Method : {order.payment_method}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time}

Products
-------------------------
{product_details}

Next Step

Please update the order status further as:

• Dispatched
• Out for Delivery
• Delivered

Thank you for using ConstructWithUs.

ConstructWithUs Platform
""",
                settings.EMAIL_HOST_USER,
                [agency_email],
                fail_silently=False
            )

    return redirect("agency_orders")



from django.core.mail import send_mail
from django.conf import settings

@login_required
def agency_dispatch_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        agency=request.user.agency_profile
    )

    if request.method == "POST":

        order.delivery.delivery_status = "Dispatched"
        order.delivery.dispatched_at = timezone.now()
        order.delivery.save()

        order.order_status = "OutForDelivery"
        order.save()

        # =========================
        # PRODUCT LIST
        # =========================

        product_details = ""

        for item in order.items.all():

            product_details += f"""
Product : {item.product_name}
Quantity : {item.quantity}
Price : ₹{item.price}
-------------------------
"""

        engineer_email = order.engineer.email
        agency_email = order.agency.user.email

        delivery_date = order.delivery.delivery_date
        delivery_time = order.delivery.delivery_time

        # =========================
        # ENGINEER MAIL
        # =========================

        send_mail(
            f"Order #{order.id} Dispatched - Out for Delivery",
            f"""
Hello {order.engineer.engineer_profile.full_name},

Good News!

Your order is now ready and has been dispatched by the agency.

Order ID : #{order.id}
Status : Out For Delivery
Payment Method : {order.payment_method}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time}

Products Ordered
-------------------------
{product_details}

Your order is currently on the way to your site.

Once the delivery agent reaches your site, they will call you.

Please verify the following when the delivery arrives:

• Check all products are delivered correctly
• Verify quantities
• Confirm product condition
• Complete payment if Cash on Delivery

After the payment Received by the Agency Owner or Agency Admin update the Order Status as delivered.

Thank you for using ConstructWithUs.

ConstructWithUs Team
""",
            settings.EMAIL_HOST_USER,
            [engineer_email],
            fail_silently=False
        )

        # =========================
        # AGENCY MAIL
        # =========================

        send_mail(
            f"Order #{order.id} Status Updated - Dispatched",
            f"""
Hello {order.agency.company_name},

The order status has been updated successfully.

Order ID : #{order.id}
Status : Out For Delivery
Payment Method : {order.payment_method}

Expected Delivery
Date : {delivery_date}
Time : {delivery_time}

Products
-------------------------
{product_details}

The delivery has been dispatched and the engineer has been notified.

Next Step

Once delivery is completed, please update the order status as:

• Delivered

Thank you for using ConstructWithUs.

ConstructWithUs Platform
""",
            settings.EMAIL_HOST_USER,
            [agency_email],
            fail_silently=False
        )

    return redirect("agency_orders")


from django.core.mail import send_mail
from django.conf import settings

@login_required
def agency_mark_delivered(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        agency=request.user.agency_profile
    )

    if request.method == "POST":

        order.delivery.delivery_status = "Delivered"
        order.delivery.delivered_at = timezone.now()
        order.delivery.save()

        order.order_status = "Delivered"
        order.save()

        # =========================
        # PRODUCT LIST
        # =========================

        product_details = ""

        for item in order.items.all():

            product_details += f"""
Product : {item.product_name}
Quantity : {item.quantity}
Price : ₹{item.price}
-------------------------
"""

        engineer_email = order.engineer.email
        agency_email = order.agency.user.email

        # =========================
        # ENGINEER MAIL
        # =========================

        send_mail(
            f"Order #{order.id} Delivered Successfully",
            f"""
Hello {order.engineer.engineer_profile.full_name},

Congratulations! Your order has been delivered successfully.

Order ID : #{order.id}
Payment Method : {order.payment_method}
Total Amount Paid : ₹{order.total_amount}

Products Delivered
-------------------------
{product_details}

We hope all products arrived safely at your site.

Thank you for choosing ConstructWithUs for your construction material needs.

We look forward to serving you again for your upcoming projects.

ConstructWithUs Team
""",
            settings.EMAIL_HOST_USER,
            [engineer_email],
            fail_silently=False
        )

        # =========================
        # AGENCY MAIL
        # =========================

        send_mail(
            f"Order #{order.id} Delivered Successfully",
            f"""
Hello {order.agency.company_name},

The delivery status for the order has been updated successfully.

Order ID : #{order.id}
Status : Delivered
Payment Method : {order.payment_method}

Products Delivered
-------------------------
{product_details}

The engineer has received the materials successfully.

Thank you for using the ConstructWithUs platform.

ConstructWithUs Platform
""",
            settings.EMAIL_HOST_USER,
            [agency_email],
            fail_silently=False
        )

    return redirect("agency_orders")