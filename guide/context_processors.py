from typing import Optional

from django.http import HttpRequest

from guide.models import UserProfile


def user_profile(request: HttpRequest) -> dict:
    profile: Optional[UserProfile] = None
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None
    return {"user_profile": profile}

