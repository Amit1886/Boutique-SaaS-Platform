from __future__ import annotations

import base64
import secrets
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import UserProfile, UserRole
from analytics.models import TemplateUsageEvent, VendorAnalytics
from boutique.models import Product, ProductCategory, TemplateDesign
from orders.models import Order, TrackingStage
from tailors.models import TailorPayment, TailorProfile, TailorReview, TailorTask, TaskStatus
from tryon_ai.models import TryOnSession, TryOnType
from vendors.models import FeatureAccess, Plan, VendorProfile
from wallet.models import TxType, WalletAccount, WalletTransaction


def _tiny_png_bytes() -> bytes:
    # Valid 1x1 transparent PNG.
    return base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7+gYkAAAAASUVORK5CYII="
    )


@dataclass(frozen=True)
class DemoCreds:
    admin_username: str
    vendor_username: str
    tailor_username: str
    customer_username: str
    password: str


class Command(BaseCommand):
    help = "Seed a complete demo flow (users/vendor/products/templates/try-on/order/tailor/wallet/analytics)."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="", help="Optional fixed password for all demo users.")
        parser.add_argument("--reset", action="store_true", help="Delete existing demo objects and recreate.")

    @transaction.atomic
    def handle(self, *args, **options):
        password = (options.get("password") or "").strip()
        if not password:
            password = secrets.token_urlsafe(12)

        creds = DemoCreds(
            admin_username="demo_admin",
            vendor_username="demo_vendor",
            tailor_username="demo_tailor",
            customer_username="demo_customer",
            password=password,
        )

        if options.get("reset"):
            self._reset_demo(creds)

        self._seed(creds)

        self.stdout.write(self.style.SUCCESS("✅ Demo data ready"))
        self.stdout.write("")
        self.stdout.write("Demo login credentials (all same password):")
        self.stdout.write(f"- Admin (Django admin): {creds.admin_username} / {creds.password}")
        self.stdout.write(f"- Vendor: {creds.vendor_username} / {creds.password}")
        self.stdout.write(f"- Tailor: {creds.tailor_username} / {creds.password}")
        self.stdout.write(f"- Customer: {creds.customer_username} / {creds.password}")
        self.stdout.write("")
        self.stdout.write("Open these URLs:")
        self.stdout.write("- Home: http://127.0.0.1:8000/")
        self.stdout.write("- Django Admin: http://127.0.0.1:8000/admin/")
        self.stdout.write("- Vendor Store: http://127.0.0.1:8000/demo/")
        self.stdout.write("- Vendor Dashboard: http://127.0.0.1:8000/vendor/")
        self.stdout.write("- Tailor Dashboard: http://127.0.0.1:8000/tailor/")
        self.stdout.write("- Customer Dashboard: http://127.0.0.1:8000/accounts/dashboard/")
        self.stdout.write("- Magic Studio: http://127.0.0.1:8000/magic/")
        self.stdout.write("")
        self.stdout.write("Notes:")
        self.stdout.write("- For Magic Studio Admin UI: set `MAGIC_ADMIN_TOKEN` in `.env`, then open /magic/ and go to Admin page inside SPA.")
        self.stdout.write("- If /magic/ shows 'SPA not built yet', build once: `cd boutique_magic_saas/frontend && npm install && npm run build`.")

    def _reset_demo(self, creds: DemoCreds) -> None:
        User = get_user_model()
        User.objects.filter(username__in=[creds.admin_username, creds.vendor_username, creds.tailor_username, creds.customer_username]).delete()
        VendorProfile.objects.filter(subdomain="demo").delete()
        Plan.objects.filter(name__in=["Free", "Standard", "Pro", "Enterprise", "Demo"]).delete()

        # Safe cleanup for demo objects by tag/name (best-effort)
        TemplateDesign.objects.filter(name__startswith="Demo ").delete()
        Product.objects.filter(name__startswith="Demo ").delete()

    def _seed(self, creds: DemoCreds) -> None:
        User = get_user_model()

        admin_user, _ = User.objects.get_or_create(
            username=creds.admin_username,
            defaults={"email": "demo_admin@example.com", "is_staff": True, "is_superuser": True},
        )
        if not admin_user.is_staff or not admin_user.is_superuser:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save(update_fields=["is_staff", "is_superuser"])
        admin_user.set_password(creds.password)
        admin_user.save(update_fields=["password"])
        UserProfile.objects.get_or_create(user=admin_user, defaults={"role": UserRole.ADMIN, "phone": "9999999999"})

        vendor_user, _ = User.objects.get_or_create(username=creds.vendor_username, defaults={"email": "demo_vendor@example.com"})
        vendor_user.set_password(creds.password)
        vendor_user.save(update_fields=["password"])
        UserProfile.objects.get_or_create(user=vendor_user, defaults={"role": UserRole.VENDOR, "phone": "8888888888"})

        tailor_user, _ = User.objects.get_or_create(username=creds.tailor_username, defaults={"email": "demo_tailor@example.com"})
        tailor_user.set_password(creds.password)
        tailor_user.save(update_fields=["password"])
        UserProfile.objects.get_or_create(user=tailor_user, defaults={"role": UserRole.TAILOR, "phone": "7777777777"})

        customer_user, _ = User.objects.get_or_create(username=creds.customer_username, defaults={"email": "demo_customer@example.com"})
        customer_user.set_password(creds.password)
        customer_user.save(update_fields=["password"])
        UserProfile.objects.get_or_create(user=customer_user, defaults={"role": UserRole.CUSTOMER, "phone": "6666666666"})

        # Plans + feature toggles
        demo_plan, _ = Plan.objects.get_or_create(name="Demo", defaults={"price": Decimal("0.00"), "features": {"demo": True}})
        for key in [
            "tryon_2d",
            "tryon_3d",
            "tryon_ar",
            "measurements_ai",
            "blouse_designer",
            "whatsapp_bot",
            "tailor_erp",
            "payroll",
            "wallet",
        ]:
            FeatureAccess.objects.get_or_create(plan=demo_plan, feature_key=key, defaults={"enabled": True})

        vendor, _ = VendorProfile.objects.get_or_create(
            subdomain="demo",
            defaults={
                "user": vendor_user,
                "business_name": "Demo Boutique",
                "theme_color": "#db2777",
                "plan": demo_plan,
                "upi_id": "demo@upi",
            },
        )
        if vendor.user_id != vendor_user.id:
            vendor.user = vendor_user
        vendor.plan = demo_plan
        vendor.save()

        # Products
        tiny = _tiny_png_bytes()
        p1 = self._product(vendor, "Demo Saree - Rose Silk", ProductCategory.SAREE, "2999.00", tiny, "Premium silk saree (demo).")
        self._product(vendor, "Demo Blouse Stitching", ProductCategory.BLOUSE, "799.00", tiny, "Stitching service (demo).")
        self._product(vendor, "Demo Fall-Pico Service", ProductCategory.FALL_PICO, "199.00", tiny, "Fall/pico service (demo).")

        # Templates
        t1 = self._template(vendor, "Demo Template - Wedding Pink", ProductCategory.SAREE, tiny, default_flag=True)
        t2 = self._template(vendor, "Demo Template - Party Blue", ProductCategory.SAREE, tiny, default_flag=False)
        self._template(vendor, "Demo Template - Bridal Purple", ProductCategory.SAREE, tiny, default_flag=False)

        # Analytics + trending events
        va, _ = VendorAnalytics.objects.get_or_create(vendor=vendor)
        va.total_orders = 1
        va.revenue = Decimal("2999.00")
        va.save()

        for ev_type in [TemplateUsageEvent.EventType.VIEW, TemplateUsageEvent.EventType.TRYON, TemplateUsageEvent.EventType.FAVORITE]:
            TemplateUsageEvent.objects.get_or_create(
                vendor=vendor,
                template=t1,
                user_id=customer_user.id,
                event_type=ev_type,
                defaults={"meta": {"demo": True}},
            )

        TemplateUsageEvent.objects.get_or_create(
            vendor=vendor,
            template=t2,
            user_id=customer_user.id,
            event_type=TemplateUsageEvent.EventType.VIEW,
            defaults={"meta": {"demo": True}},
        )

        # Try-on session (dummy images)
        session = TryOnSession.objects.filter(vendor=vendor, user=customer_user).first()
        if not session:
            session = TryOnSession(vendor=vendor, user=customer_user, type=TryOnType.TWO_D, selected_template=t1)
            session.original_image.save("demo_original.png", ContentFile(tiny), save=False)
            session.bg_removed_image.save("demo_bg_removed.png", ContentFile(tiny), save=False)
            session.ai_result.save("demo_result.png", ContentFile(tiny), save=False)
            session.measurement_data = {"bust": 34, "waist": 28, "hips": 36, "shoulder": 14}
            session.save()

        # Order
        order = Order.objects.filter(vendor=vendor, user=customer_user).first()
        if not order:
            order = Order.objects.create(
                vendor=vendor,
                user=customer_user,
                product=p1,
                tryon_session=session,
                amount=Decimal("2999.00"),
                status="Confirmed",
                tracking_stage=TrackingStage.CUTTING,
            )

        # Tailor side
        tailor_profile, _ = TailorProfile.objects.get_or_create(
            user=tailor_user, vendor=vendor, defaults={"speciality": "Blouse + Saree", "daily_capacity": 7, "avg_rating": 4.8, "rating_count": 21}
        )
        TailorTask.objects.get_or_create(
            tailor=tailor_profile,
            order=order,
            defaults={"task_type": "Stitching", "status": TaskStatus.IN_PROGRESS, "piece_rate": Decimal("250.00")},
        )

        TailorPayment.objects.get_or_create(
            tailor=tailor_profile,
            period_start=date.today().replace(day=1),
            period_end=date.today(),
            defaults={"pieces_done": 3, "amount": Decimal("750.00")},
        )

        TailorReview.objects.get_or_create(
            order=order,
            tailor=tailor_profile,
            defaults={"user": customer_user, "rating": 5, "comment": "Perfect fitting! (demo)"},
        )

        # Wallet
        wallet, _ = WalletAccount.objects.get_or_create(user=customer_user, defaults={"balance": Decimal("200.00")})
        if wallet.balance < Decimal("200.00"):
            wallet.balance = Decimal("200.00")
            wallet.save(update_fields=["balance"])
        WalletTransaction.objects.get_or_create(
            wallet=wallet,
            tx_type=TxType.CASHBACK,
            amount=Decimal("50.00"),
            defaults={"note": "Demo cashback", "meta": {"order_id": order.id}},
        )

    def _product(self, vendor: VendorProfile, name: str, category: str, price: str, img: bytes, desc: str) -> Product:
        obj = Product.objects.filter(vendor=vendor, name=name).first()
        if obj:
            return obj
        obj = Product(vendor=vendor, name=name, category=category, price=Decimal(price), description=desc, stock_meter=Decimal("50.00"))
        obj.image.save(f"{name.lower().replace(' ', '_')}.png", ContentFile(img), save=False)
        obj.save()
        return obj

    def _template(self, vendor: VendorProfile, name: str, category: str, img: bytes, default_flag: bool) -> TemplateDesign:
        obj = TemplateDesign.objects.filter(vendor=vendor, name=name).first()
        if obj:
            return obj
        obj = TemplateDesign(vendor=vendor, name=name, category=category, default_flag=default_flag, fit_meta={"demo": True})
        obj.image.save(f"{name.lower().replace(' ', '_')}.png", ContentFile(img), save=False)
        obj.save()
        return obj
