from django.db import models


class Category(models.TextChoices):
    SAREE = "saree", "Saree"
    BLOUSE = "blouse", "Blouse"
    FALL = "fall", "Fall-Pico"
    LEHENGA = "lehenga", "Lehenga"
    CUSTOM = "custom", "Custom"


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class TemplateDesign(models.Model):
    image = models.ImageField(upload_to="templates/")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)

    def __str__(self) -> str:
        return self.name


class TryOnStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"


class TryOnRequest(models.Model):
    user_image = models.ImageField(upload_to="tryon/user/")
    selected_template = models.ForeignKey(
        TemplateDesign, on_delete=models.SET_NULL, null=True, blank=True
    )
    auto_generated_image = models.ImageField(
        upload_to="tryon/generated/", null=True, blank=True
    )
    bust_size = models.DecimalField(max_digits=6, decimal_places=2)
    waist_size = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=TryOnStatus.choices, default=TryOnStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"TryOnRequest #{self.pk}"


class OrderStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    PROCESSING = "Processing", "Processing"
    COMPLETED = "Completed", "Completed"
    CANCELED = "Canceled", "Canceled"


class Order(models.Model):
    tryon_request = models.ForeignKey(TryOnRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )

    def __str__(self) -> str:
        return f"Order #{self.pk}"

