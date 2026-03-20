from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta



# Create your models here.
class Engineerprofile(models.Model):

     # ===== LINK TO USER (1 engineer = 1 user) =====
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="engineer_profile"
    )

    # ===== BASIC DETAILS =====
    email = models.EmailField(null=False, blank=False)

    # ===== EDUCATIONAL DETAILS =====
    DEGREE_CHOICES = [
        ('BE', 'BE'),
        ('ME', 'ME'),
        ('MTech', 'BTech'),
        ('MTech', 'MTech'),
        ('Diploma', 'Diploma'),
        ('PhD', 'PhD'),
        ('Others', 'Others'),
    ]

    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        null=False,
        blank=False
    )

    other_degree = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    college_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    clg_district = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    degree_certificate = models.FileField(
        upload_to='engineer_certificates/',
        null=False,
        blank=False
    )

    # ===== PERSONAL DETAILS =====
    full_name = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )

    age = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=False,
        blank=False
    )

    date_of_birth = models.DateField(
        null=False,
        blank=False
    )

    phone_number = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False

    )

    address = models.TextField(
        null=False,
        blank=False
    )

    district = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    state = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    pincode = models.CharField(
        max_length=10,
        null=False,
        blank=False
    )
    terms_accepted = models.BooleanField(default=False)

    # ===== META =====
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
gst_validator = RegexValidator(
    regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
    message="Enter a valid GST number"
)



class AgencyProfile(models.Model):

    # ===== LINK TO USER =====
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="agency_profile"
    )

    # ===== COMPANY DETAILS =====
    company_name = models.CharField(max_length=255)

    gst_number = models.CharField(max_length=50)
    gst_certificate = models.FileField(
        upload_to="agency_gst_certificates/"
    )

    company_phone = models.CharField(
        max_length=15,
        unique=True
    )

    company_address = models.TextField()
    company_district = models.CharField(max_length=100)
    company_state = models.CharField(max_length=100)
    company_pincode = models.CharField(max_length=6)

    # ===== OWNER DETAILS =====
    owner_name = models.CharField(max_length=150)
    owner_email = models.EmailField()

    owner_phone = models.CharField(
        max_length=15,
        unique=True
    )

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    owner_age = models.PositiveIntegerField()
    owner_dob = models.DateField()
    owner_address = models.TextField()
    owner_district = models.CharField(max_length=100)
    owner_state = models.CharField(max_length=100)
    owner_pincode = models.CharField(max_length=6)

    # ===== AUTO APPROVAL =====
    status = models.CharField(
        max_length=20,
        default="approved"
    )

    approved_at = models.DateTimeField(
        default=timezone.localtime
    )

    terms_accepted = models.BooleanField(default=False)

    # ===== META =====
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if self.company_district:
            self.company_district = self.company_district.strip().upper()

        if self.owner_district:
            self.owner_district = self.owner_district.strip().upper()

        if self.company_state:
            self.company_state = self.company_state.strip().upper()

        if self.owner_state:
            self.owner_state = self.owner_state.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name   

    def save(self, *args, **kwargs):
        if self.company_district:
         self.company_district = self.company_district.upper()
        super().save(*args, **kwargs) 


from django.db import models
from django.utils import timezone

class Product(models.Model):

    PRODUCT_TYPE_CHOICES = [
        ('cement', 'Cement'),
        ('steel', 'Steel'),
        ('bricks', 'Bricks'),
        ('sand','sand'),
        ('others', 'Others'),
    ]

    # ===== LINK TO AGENCY =====
    agency = models.ForeignKey(
        AgencyProfile,
        on_delete=models.CASCADE,
        related_name="products"
    )

    # ===== PRODUCT INFO =====
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES
    )

    other_product_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Required if product type is Others"
    )

    brand_name = models.CharField(max_length=150)

     # ✅ ADD THIS FIELD
    product_name = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    # ===== LOCATION =====
    address = models.TextField()
    district = models.TextField(default="TIRUPUR")
    pincode = models.CharField(max_length=6)

    # ===== META =====
    created_at = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return f"{self.brand_name} - {self.product_name} ({self.product_type})"
    


from django.db import models
class ProductVariants(models.Model):

    UNIT_CHOICES = [
        ('bag', 'Bag'),
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('piece', 'Piece'),
    ]

    # ===== LINK TO PRODUCT =====
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    spc_product_name = models.CharField(
        max_length=200
    )

    # ===== VARIATION DETAILS =====
    size_or_weight = models.CharField(
        max_length=50,
        help_text="Ex: 50kg, 25kg, 8mm, 12mm"
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        help_text="Available stock count"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.size_or_weight} {self.unit}"



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ConstructionSite(models.Model):

    SITE_CATEGORY_CHOICES = [
        ('house', 'House'),
        ('building', 'Building'),
        ('flats', 'Flats'),
        ('commercial', 'Commercial Stores'),
        ('others', 'Others'),
    ]

    engineer = models.ForeignKey( User,
        on_delete=models.CASCADE,
        related_name="engineer_sites"
    )

    # ===== SITE BASIC DETAILS =====
    site_name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=SITE_CATEGORY_CHOICES
    )

    other_category = models.CharField(
    max_length=100,
    null=True,
    blank=True
)

    total_sqft = models.FloatField()

    site_map = models.FileField(
    upload_to='site_maps/',
    null=True,
    blank=True
)

    blueprint_file = models.FileField(
    upload_to='site_blueprints/',
    null=True,
    blank=True
)

    building_area_sqft = models.FloatField()

    approximate_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    start_date = models.DateField()
    end_date = models.DateField()

    STATUS_CHOICES = [
    ('Planning', 'Planning'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('NearComplete', 'Near To Complete'),
    ('Completed', 'Completed'),
    ('HandedOver', 'Handed Over'),
]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='Planning'
)

    description = models.TextField(blank=True)
    # ===== LOCATION =====
    site_address = models.TextField()
    site_district = models.CharField(max_length=100)
    site_state = models.CharField(max_length=100)
    site_pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if self.site_district:
            self.site_district = self.site_district.strip().upper()
        super().save(*args, **kwargs)
        
        return self.site_name


class SiteOwner(models.Model):

    site = models.OneToOneField(
        ConstructionSite,
        on_delete=models.CASCADE,
        related_name="owner"
    )

    owner_name = models.CharField(max_length=150)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    owner_gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    owner_phone = models.CharField(max_length=15)

    owner_address = models.TextField()
    owner_district = models.CharField(max_length=100)
    owner_pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.owner_name



class CartItem(models.Model):

    site = models.ForeignKey(
        ConstructionSite,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    variant = models.ForeignKey(
        ProductVariants,
        on_delete=models.CASCADE
    )

    product_name = models.CharField(max_length=200)

    weight_or_size = models.CharField(max_length=100)

    average_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        return self.average_price * self.quantity

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"
    

    
class QuotationRequest(models.Model):

    site = models.ForeignKey(
        ConstructionSite,
        on_delete=models.CASCADE
    )

    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    agency = models.ForeignKey(
        AgencyProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    request_note = models.TextField()

    DELIVERY_CHOICES = [
("urgent","Urgent (1-2 days)"),
("3days","Within 3 days"),
("7days","Within 1 week"),
("flexible","Flexible"),
]

    delivery_preference = models.CharField(
    max_length=20,
    choices=DELIVERY_CHOICES ,default="flexible"
)

    expected_delivery_date = models.DateField(
    default=timezone.now
) 

    estimated_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("Requested", "Requested"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Expired","Expired"),
        ("MOVED_For_Order", "Converted To Order"),  # 🔥 add this
    ]

    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Requested"
    )

    def default_valid_until():

        now = timezone.localtime()

        today_8pm = now.replace(
        hour=20,
        minute=0,
        second=0,
        microsecond=0
    )

    # If already past 9 PM → set tomorrow 8 PM
        if now > today_8pm:
            today_8pm = today_8pm + timedelta(days=1)

        return today_8pm
    
    quotation_valid_until = models.DateTimeField(
    default=default_valid_until
)


    def __str__(self):
        return f"Quotation #{self.id}"


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        QuotationRequest,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_name = models.CharField(max_length=200)
    weight_or_size = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity


class EstimatedQuotation(models.Model):

    quotation = models.OneToOneField(
        QuotationRequest,
        on_delete=models.CASCADE,
        related_name="final_estimate"
    )
    

    base_total = models.DecimalField(max_digits=12, decimal_places=2)

    transport_charge = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_percent = models.DecimalField(max_digits=5, decimal_places=2)
    sgst_percent = models.DecimalField(max_digits=5, decimal_places=2)
    platform_fee_percent = models.DecimalField(max_digits=5, decimal_places=2)

    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee_amount = models.DecimalField(max_digits=10, decimal_places=2)

    final_total = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)


class FinalQuotationItem(models.Model):

    final_estimate = models.ForeignKey(
        EstimatedQuotation,
        on_delete=models.CASCADE,
        related_name="final_items"
    )

    product_name = models.CharField(max_length=200)
    weight_or_size = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.final_price * self.quantity

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):

    ORDER_STATUS_CHOICES = [
    ("Placed", "Placed"),
    ("AgencyApproved", "Agency Approved"),
    ("AgencyRejected", "Agency Rejected"),
    ("Processing", "Processing"),
    ("OutForDelivery", "Out For Delivery"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
]


    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
    ]

    quotation = models.ForeignKey(
        "QuotationRequest",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="engineer_orders"
    )

    agency = models.ForeignKey(
        "AgencyProfile",
        on_delete=models.CASCADE,
        related_name="agency_orders"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    # COD confirmation
    cod_confirmed = models.BooleanField(default=False)
    cod_confirmed_at = models.DateTimeField(null=True, blank=True)

    order_status = models.CharField(
    max_length=30,
    choices=ORDER_STATUS_CHOICES,
    default="Placed"
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product_name} - Order #{self.order.id}"


class OrderDelivery(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery"
    )

    delivery_date = models.DateField()
    delivery_time = models.TimeField()

    engineer_name = models.CharField(max_length=150)
    engineer_phone = models.CharField(max_length=20)

    site_owner_phone = models.CharField(max_length=20)

    site_address = models.TextField()
    site_district = models.CharField(max_length=100)
    site_pincode = models.CharField(max_length=10)

    delivery_status = models.CharField(
        max_length=30,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)  # 🔥 add this



    def __str__(self):
        return f"Delivery for Order #{self.order.id}"
