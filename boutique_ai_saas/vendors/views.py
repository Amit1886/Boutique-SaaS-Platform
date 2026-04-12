from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile, UserRole
from orders.models import Order, TrackingStage
from tailors.models import TailorProfile, TailorTask, TaskStatus

from .models import Plan, VendorProfile
from .forms import VendorSettingsForm


def pricing(request):
    plans = Plan.objects.all().order_by("price")
    return render(request, "pricing_plans.html", {"plans": plans})


@login_required
def vendor_dashboard(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        messages.error(request, "Vendor profile not found.")
        return redirect("home")
    from analytics.models import VendorAnalytics
    from orders.models import Order
    from tryon_ai.models import TryOnSession
    from boutique.models import Product

    analytics, _ = VendorAnalytics.objects.get_or_create(vendor=vendor)
    stats = {
        "products": Product.objects.filter(vendor=vendor).count(),
        "orders": Order.objects.filter(vendor=vendor).count(),
        "tryon_sessions": TryOnSession.objects.filter(vendor=vendor).count(),
        "revenue": analytics.revenue,
    }
    from .models import FeatureAccess

    enabled_features = set(
        FeatureAccess.objects.filter(plan=vendor.plan, enabled=True).values_list("feature_key", flat=True)
    ) if vendor.plan_id else set()

    settings_form = VendorSettingsForm(instance=vendor)
    return render(
        request,
        "dashboard_vendor.html",
        {
            "vendor": vendor,
            "analytics": analytics,
            "stats": stats,
            "settings_form": settings_form,
            "enabled_features": enabled_features,
        },
    )


@login_required
@require_http_methods(["POST"])
def vendor_settings_update(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        return redirect("home")
    form = VendorSettingsForm(request.POST, instance=vendor)
    if form.is_valid():
        form.save()
        messages.success(request, "Settings updated.")
    return redirect("vendor_dashboard")


@login_required
@require_http_methods(["POST"])
def upgrade_plan(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        return redirect("home")
    plan_id = request.POST.get("plan_id")
    plan = Plan.objects.filter(pk=plan_id).first()
    if not plan:
        messages.error(request, "Invalid plan.")
        return redirect("pricing")
    vendor.plan = plan
    vendor.save(update_fields=["plan"])
    messages.success(request, f"Plan updated to {plan.name}. (Payment integration is dummy for now)")
    profile = UserProfile.objects.filter(user=request.user).first()
    if profile and profile.role != UserRole.VENDOR:
        profile.role = UserRole.VENDOR
        profile.save(update_fields=["role"])
    return redirect("vendor_dashboard")


@login_required
@require_http_methods(["GET", "POST"])
def vendor_tailor_tasks(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        messages.error(request, "Vendor profile not found.")
        return redirect("home")

    tailors = TailorProfile.objects.filter(vendor=vendor).select_related("user").order_by("user__username")[:200]
    orders = (
        Order.objects.filter(vendor=vendor)
        .select_related("product")
        .prefetch_related(Prefetch("tailor_tasks", queryset=TailorTask.objects.select_related("tailor", "tailor__user").order_by("-id")))
        .order_by("-id")[:200]
    )

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        tailor_id = request.POST.get("tailor_id")
        task_type = (request.POST.get("task_type") or "Cutting").strip()[:80]
        piece_rate = request.POST.get("piece_rate") or "0"
        deadline = request.POST.get("deadline") or None

        order = Order.objects.filter(pk=order_id, vendor=vendor).first()
        tailor = TailorProfile.objects.filter(pk=tailor_id, vendor=vendor).first()
        if not order or not tailor:
            messages.error(request, "Invalid order/tailor.")
            return redirect("vendor_tailor_tasks")

        try:
            from decimal import Decimal

            rate = Decimal(str(piece_rate))
        except Exception:
            rate = 0

        TailorTask.objects.create(
            tailor=tailor,
            order=order,
            task_type=task_type,
            status=TaskStatus.PENDING,
            deadline=deadline,
            piece_rate=rate,
        )
        messages.success(request, "Task assigned.")
        return redirect("vendor_tailor_tasks")

    return render(request, "vendor_tasks.html", {"vendor": vendor, "tailors": tailors, "orders": orders})
