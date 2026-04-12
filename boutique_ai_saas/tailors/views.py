from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from accounts.models import UserProfile, UserRole

from .models import PaymentStatus, TailorPayment, TailorProfile, TailorTask, TaskStatus


@login_required
def tailor_dashboard(request):
    tailor = TailorProfile.objects.filter(user=request.user).select_related("vendor").first()
    if not tailor:
        messages.error(request, "Tailor profile not found.")
        return redirect("home")

    tasks = TailorTask.objects.filter(tailor=tailor).select_related("order", "order__product").order_by("-id")[:200]
    return render(request, "dashboard_tailor.html", {"tailor": tailor, "tasks": tasks})


@login_required
@require_http_methods(["POST"])
def update_task_status(request):
    task_id = request.POST.get("task_id")
    status = request.POST.get("status")
    tailor = TailorProfile.objects.filter(user=request.user).first()
    if not tailor:
        return redirect("tailor_dashboard")
    valid = {k for k, _ in TaskStatus.choices}
    task = TailorTask.objects.filter(pk=task_id, tailor=tailor).first()
    if task and status in valid:
        task.status = status
        if status == TaskStatus.DONE and task.completed_at is None:
            task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at"])
        messages.success(request, "Task updated.")
    return redirect("tailor_dashboard")


@login_required
def payroll(request):
    tailor = TailorProfile.objects.filter(user=request.user).select_related("vendor").first()
    if not tailor:
        messages.error(request, "Tailor profile not found.")
        return redirect("home")

    # Current month period
    today = date.today()
    period_start = date(today.year, today.month, 1)
    period_end = today

    tasks = (
        TailorTask.objects.filter(tailor=tailor, status=TaskStatus.DONE, completed_at__date__gte=period_start, completed_at__date__lte=period_end)
        .select_related("order", "order__product")
        .order_by("-completed_at")[:500]
    )

    default_rates = {
        "Cutting": Decimal("50.00"),
        "Stitching": Decimal("80.00"),
        "Finishing": Decimal("40.00"),
        "Fall-Pico": Decimal("30.00"),
    }
    total = Decimal("0.00")
    pieces = 0
    for t in tasks:
        rate = t.piece_rate if t.piece_rate and t.piece_rate > 0 else default_rates.get(t.task_type, Decimal("50.00"))
        total += rate
        pieces += 1

    payments = TailorPayment.objects.filter(tailor=tailor).order_by("-id")[:50]

    if request.method == "POST":
        existing = TailorPayment.objects.filter(tailor=tailor, period_start=period_start, period_end=period_end).first()
        if existing:
            messages.info(request, "Payroll already generated for this period.")
            return redirect("tailor_payroll")
        TailorPayment.objects.create(
            tailor=tailor,
            period_start=period_start,
            period_end=period_end,
            pieces_done=pieces,
            amount=total,
            status=PaymentStatus.PENDING,
            meta={"task_count": pieces},
        )
        messages.success(request, "Payroll generated (pending).")
        return redirect("tailor_payroll")

    return render(
        request,
        "payroll.html",
        {
            "tailor": tailor,
            "tasks": tasks,
            "period_start": period_start,
            "period_end": period_end,
            "pieces": pieces,
            "total": total,
            "payments": payments,
        },
    )


@login_required
@require_http_methods(["POST"])
def mark_paid(request):
    tailor = TailorProfile.objects.filter(user=request.user).first()
    if not tailor:
        return redirect("tailor_payroll")
    payment_id = request.POST.get("payment_id")
    p = TailorPayment.objects.filter(pk=payment_id, tailor=tailor).first()
    if p and p.status != PaymentStatus.PAID:
        p.status = PaymentStatus.PAID
        p.paid_at = timezone.now()
        p.save(update_fields=["status", "paid_at"])
        messages.success(request, "Marked as paid.")
    return redirect("tailor_payroll")
