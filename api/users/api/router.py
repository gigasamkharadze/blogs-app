from ninja import Router
from config.auth import AuthBearer
from .schemas import (
    TokenSchema,
    UserProfileSchema,
    ErrorSchema,
    SuccessSchema,
)
from .endpoints import (
    register,
    login,
    update_profile,
    upload_profile_image,
    get_profile,
    change_password,
    request_password_reset,
    confirm_password_reset
)

router = Router(tags=["Users"])

router.add_api_operation(
    "/register",
    ["POST"],
    register,
    response={201: UserProfileSchema, 400: ErrorSchema},
    auth=None,
    summary="Register new user"
)

router.add_api_operation(
    "/token",
    ["POST"],
    login,
    response={200: TokenSchema, 401: ErrorSchema},
    auth=None,
    summary="Login to get token"
)

router.add_api_operation(
    "/profile",
    ["GET"],
    get_profile,
    response=UserProfileSchema,
    auth=AuthBearer(),
    summary="Get user profile"
)

router.add_api_operation(
    "/profile",
    ["PUT"],
    update_profile,
    response={200: UserProfileSchema, 400: ErrorSchema},
    auth=AuthBearer(),
    summary="Update user profile"
)

router.add_api_operation(
    "/profile/image",
    ["POST"],
    upload_profile_image,
    response={200: SuccessSchema, 400: ErrorSchema},
    auth=AuthBearer(),
    summary="Upload profile image"
)

router.add_api_operation(
    "/change-password",
    ["POST"],
    change_password,
    response={200: SuccessSchema, 400: ErrorSchema},
    auth=AuthBearer(),
    summary="Change password for authenticated user"
)

router.add_api_operation(
    "/reset-password",
    ["POST"],
    request_password_reset,
    response={200: SuccessSchema, 404: ErrorSchema, 500: ErrorSchema},
    summary="Request password reset via email"
)

router.add_api_operation(
    "/reset-password/confirm",
    ["POST"],
    confirm_password_reset,
    response={200: SuccessSchema, 400: ErrorSchema},
    summary="Set new password with reset token"
)