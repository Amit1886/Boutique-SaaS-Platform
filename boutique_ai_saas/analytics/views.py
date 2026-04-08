from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from vendors.models import VendorProfile

from .models import VendorAnalytics


@login_required
def vendor_analytics(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        return redirect("home")
    analytics, _ = VendorAnalytics.objects.get_or_create(vendor=vendor)
    return render(request, "dashboard_vendor.html", {"vendor": vendor, "analytics": analytics, "analytics_tab": True})


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    vendors = VendorProfile.objects.select_related("plan").order_by("business_name")
    analytics = VendorAnalytics.objects.select_related("vendor").order_by("-revenue")[:50]
    return render(request, "dashboard_admin.html", {"vendors": vendors, "analytics": analytics})

