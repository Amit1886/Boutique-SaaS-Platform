# Boutique Pro (Django)

## Setup

1. `cd boutique_pro`
2. Create and activate a virtualenv
3. Install deps: `pip install -r requirements.txt`
4. Run migrations (auto-seeds demo products + templates): `python manage.py migrate`
5. Create admin user: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## Pages

- `/` Home
- `/products/<category>/` Product listing
- `/tryon/upload/` Upload photo + measurements
- `/tryon/templates/<id>/` Horizontal template gallery + live overlay preview
- `/tryon/generate/` Generate dummy try-on output
- `/order/confirm/` Confirm + place order
- `/admin/orders/` Simple staff-only order dashboard
- `/admin/` Django admin
- `/api/` DRF API (products, templates, try-on requests, orders)

## Dummy AI hooks

- `boutiqueapp/ai.py`:
  - `remove_background()` (placeholder background removal)
  - `generate_virtual_tryon()` (placeholder overlay compositor)

