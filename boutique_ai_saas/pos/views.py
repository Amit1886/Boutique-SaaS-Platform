import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from vendors.models import VendorProfile

from .forms import POSForm
from .models import POSOrder


@login_required
@require_http_methods(["GET", "POST"])
def pos_billing(request):
    vendor = VendorProfile.objects.filter(user=request.user).first()
    if not vendor:
        messages.error(request, "Vendor profile required.")
        return redirect("home")

    if request.method == "POST":
        form = POSForm(request.POST)
        if form.is_valid():
            try:
                items = json.loads(form.cleaned_data["item_list_json"] or "[]")
                total = sum(float(i.get("qty", 1)) * float(i.get("price", 0)) for i in items)
            except Exception:
                messages.error(request, "Invalid JSON items.")
                return render(request, "pos.html", {"vendor": vendor, "form": form, "orders": []})

            POSOrder.objects.create(
                vendor=vendor,
                name=form.cleaned_data["name"],
                phone=form.cleaned_data.get("phone") or "",
                item_list=items,
                total=str(round(total, 2)),
            )
            messages.success(request, "POS bill saved.")
            return redirect("pos_billing")
    else:
        form = POSForm(initial={"item_list_json": '[{"name":"Saree","qty":1,"price":2499}]'})

    orders = POSOrder.objects.filter(vendor=vendor).order_by("-id")[:50]
    return render(request, "pos.html", {"vendor": vendor, "form": form, "orders": orders})

