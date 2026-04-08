from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from vendors.models import VendorProfile

from .forms import FabricStockForm
from .models import FabricStock


@login_required
@require_http_methods(["GET", "POST"])
def inventory_dashboard(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        messages.error(request, "Vendor profile required.")
        return redirect("home")

    if request.method == "POST":
        form = FabricStockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vendor = vendor
            obj.save()
            messages.success(request, "Fabric stock saved.")
            return redirect("inventory_dashboard")
    else:
        form = FabricStockForm()

    items = FabricStock.objects.filter(vendor=vendor).order_by("fabric_type")
    return render(request, "inventory.html", {"vendor": vendor, "form": form, "items": items})


@login_required
@require_http_methods(["POST"])
def inventory_update(request, id: int):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        return redirect("home")
    item = get_object_or_404(FabricStock, pk=id, vendor=vendor)
    form = FabricStockForm(request.POST, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated.")
    return redirect("inventory_dashboard")

