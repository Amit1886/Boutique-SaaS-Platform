from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile, UserRole

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
