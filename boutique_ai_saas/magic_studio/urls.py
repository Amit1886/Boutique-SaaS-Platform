from django.urls import path, re_path

from . import views

urlpatterns = [
    # Upload serving (React uses /uploads/* URLs)
    path("uploads/<path:path>", views.serve_upload, name="magic_uploads"),
    # API
    path("api/health", views.health, name="magic_health"),
    path("api/sarees", views.sarees, name="magic_sarees"),
    path("api/sarees/<int:item_id>", views.saree_detail, name="magic_saree_detail"),
    path("api/blouses", views.blouses, name="magic_blouses"),
    path("api/blouses/<int:item_id>", views.blouse_detail, name="magic_blouse_detail"),
    path("api/accessories", views.accessories, name="magic_accessories"),
    path("api/accessories/<int:item_id>", views.accessory_detail, name="magic_accessory_detail"),
    path("api/upload/saree-layer", views.upload_saree_layer, name="magic_upload_saree_layer"),
    path("api/upload/blouse-template", views.upload_blouse_template, name="magic_upload_blouse_template"),
    path("api/upload/accessory", views.upload_accessory, name="magic_upload_accessory"),
    path("api/gallery/looks", views.gallery_looks, name="magic_gallery_looks"),
    path("api/gallery/save", views.gallery_save, name="magic_gallery_save"),
    path("api/3d/mannequin", views.mannequin, name="magic_mannequin"),
    path("api/theme/festival", views.festival, name="magic_festival"),
    path("api/user/moodboard", views.user_moodboard, name="magic_moodboard"),
    path("api/look/share", views.look_share, name="magic_look_share"),
    path("api/uxflags", views.uxflags, name="magic_uxflags"),
    # Admin token-protected
    path("api/admin/uxflags", views.admin_uxflags, name="magic_admin_uxflags"),
    path("api/admin/uxflags/<str:key>", views.admin_uxflag_set, name="magic_admin_uxflag_set"),
    path("api/admin/festivals", views.admin_festivals, name="magic_admin_festivals"),
    # SPA
    re_path(r"^.*$", views.spa, name="magic_spa"),
]

