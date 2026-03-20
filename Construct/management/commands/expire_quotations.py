from django.core.management.base import BaseCommand
from django.utils import timezone
from Construct.models import QuotationRequest
from django.core.mail import send_mail
from django.conf import settings
from datetime import time


class Command(BaseCommand):
    help = "Expire quotations exactly after 8 PM"

    def handle(self, *args, **kwargs):

        now = timezone.localtime()

        # Only run after 8 PM
        if now.time() < time(20, 0):
            print("Not 8 PM yet")
            return

        expired_quotes = QuotationRequest.objects.filter(
            quotation_valid_until__lt=now,
            status="Approved"
        )

        for quotation in expired_quotes:

            quotation.status = "Expired"
            quotation.save()

            engineer = quotation.engineer

            send_mail(
                f"Quotation #{quotation.id} Expired",
                f"""
Hello {engineer.get_full_name() or engineer.username},

Your quotation ID #{quotation.id} has expired.

Validity Time:
{quotation.quotation_valid_until}

if you want new quotation for the same products ,click regenerate bill option at the quotation relires by agency section inside the  view final bill button

Please request a new quotation to place the order.

thank you for using ConstructWithUs ,
ConstructWithUs Team
""",
                settings.EMAIL_HOST_USER,
                [engineer.email],
                fail_silently=True
            )

        self.stdout.write(self.style.SUCCESS("Expired quotations updated"))