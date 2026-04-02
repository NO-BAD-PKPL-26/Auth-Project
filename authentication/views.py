import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import UserPreference

logger = logging.getLogger(__name__)

# email anggota kelompok
GROUP_MEMBER_EMAILS = {
    "alfino.feriza@gmail.com"
}

def is_group_member(user):
    return (
        user.is_authenticated
        and user.email
        and user.email.lower() in GROUP_MEMBER_EMAILS
    )


def home_view(request):
    
    "Jika user sudah login, ambil preferensi tampilannya."
    preference = None
    if request.user.is_authenticated:
        preference, _ = UserPreference.objects.get_or_create(user=request.user)

    return render(request, "landing_page/home.html", {
        "preference": preference,
        "is_group_member": is_group_member(request.user),
    })


ALLOWED_FONTS = {"inria-serif", "inter", "roboto", "plus-jakarta", "petrona"}



@login_required         
@require_POST          
def update_preferences_view(request):

    "Hanya group member yang bisa merubah tampilan"
    if not is_group_member(request.user):
        logger.warning(f"Unauthorized preference change attempt by {request.user.email}")
        return JsonResponse(
            {"success": False, "message": "Only group members can change preferences."},
            status=403
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    dark_mode = body.get("dark_mode")
    font = body.get("font")

    # Validasi: pastikan tidak ada field asing yang masuk
    allowed_keys = {"dark_mode", "font"}
    if not set(body.keys()).issubset(allowed_keys):
        return JsonResponse({"success": False, "message": "Unknown fields in request"}, status=400)

    # Ambil preferensi milik user yang sedang login (authorization by ownership)
    preference, _ = UserPreference.objects.get_or_create(user=request.user)

    if dark_mode is not None:
        if not isinstance(dark_mode, bool):
            return JsonResponse({"success": False, "message": "dark_mode must be boolean"}, status=400)
        preference.dark_mode = dark_mode

    if font is not None:
        if font not in ALLOWED_FONTS:
            return JsonResponse({"success": False, "message": "Invalid font choice"}, status=400)
        preference.font = font

    preference.save()

    logger.info(f"Preferences updated for user {request.user.email}")

    return JsonResponse({
        "success": True,
        "dark_mode": preference.dark_mode,
        "font": preference.font,
    })