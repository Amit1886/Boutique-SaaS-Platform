from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from vendors.models import Plan, VendorProfile

from .forms import LoginForm, ProfileLanguageForm, VendorSignupForm
from .models import UserProfile, UserRole


@require_http_methods(["GET", "POST"])
def signup_vendor(request):
    if request.method == "POST":
        form = VendorSignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "signup_vendor.html", {"form": form})

            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data.get("email") or "",
                password=form.cleaned_data["password"],
            )
            profile = UserProfile.objects.get(user=user)
            profile.role = UserRole.VENDOR
            profile.save(update_fields=["role"])

            plan = Plan.objects.filter(name__iexact="Free").first() or Plan.objects.first()
            base_slug = form.cleaned_data["subdomain"]
            slug = base_slug
            n = 2
            while VendorProfile.objects.filter(subdomain=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            VendorProfile.objects.create(
                user=user,
                business_name=form.cleaned_data["business_name"],
                subdomain=slug,
                theme_color=form.cleaned_data["theme_color"],
                plan=plan,
            )

            login(request, user)
            return redirect("vendor_dashboard")
    else:
        form = VendorSignupForm()
    return render(request, "signup_vendor.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
        messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm(request)
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
@require_http_methods(["GET", "POST"])
def language_settings(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileLanguageForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Language updated.")
            return redirect("language_settings")
    else:
        form = ProfileLanguageForm(instance=profile)
    return render(request, "language.html", {"form": form})


@login_required
def customer_dashboard(request):
    from boutique.models import SavedLook
    from orders.models import Order

    looks = SavedLook.objects.filter(user=request.user).select_related("vendor").order_by("-id")[:100]
    orders = Order.objects.filter(user=request.user).select_related("vendor", "product").order_by("-id")[:100]
    return render(request, "customer_dashboard.html", {"looks": looks, "orders": orders})
