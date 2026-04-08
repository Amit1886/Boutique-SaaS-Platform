from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile, UserRole

from .models import TailorProfile, TailorTask, TaskStatus


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
        task.save(update_fields=["status"])
        messages.success(request, "Task updated.")
    return redirect("tailor_dashboard")

