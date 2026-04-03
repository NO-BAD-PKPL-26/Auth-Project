from django.shortcuts import render

from authentication.models import UserPreference
from authentication.views import is_group_member

# Create your views here.
def landing_page(request):
    preference = None
    if request.user.is_authenticated:
        preference, _ = UserPreference.objects.get_or_create(user=request.user)

    return render(request, 'landing_page.html', {
        'preference': preference,
        'is_group_member': is_group_member(request.user),
    })