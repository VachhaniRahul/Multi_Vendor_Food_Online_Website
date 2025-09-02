from vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.select_related("user", "user_profile").get(
            user=request.user
        )
    except Exception:
        vendor = None
    context = {"vendor": vendor}
    return context
