from ninja import File
from ninja.files import UploadedFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from datetime import datetime, timedelta
from jose import jwt
import secrets
from django.conf import settings
from django.template.loader import render_to_string
import string
from .schemas import (
    AuthSchema,
    RegisterSchema,
    UserUpdateSchema,
    PasswordChangeSchema,
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema
)

User = get_user_model()


def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return 400, {"message": "Username already exists"}
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "Email already registered"}

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name or "",
        last_name=data.last_name or ""
    )
    return 201, user


def login(request, data: AuthSchema):
    user = get_object_or_404(User, username=data.username)
    if user.check_password(data.password):
        token = jwt.encode(
            {
                'username': user.username,
                'exp': datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return 200, {'access_token': token, 'token_type': 'bearer'}
    return 401, {'message': 'Invalid credentials'}


def update_profile(request, data: UserUpdateSchema):
    user = request.auth
    if data.email and User.objects.exclude(id=user.id).filter(email=data.email).exists():
        return 400, {"message": "Email already registered"}

    if data.email:
        user.email = data.email
    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    user.save()
    return 200, user


def upload_profile_image(request, file: UploadedFile = File(...)):
    user = request.auth
    user.profile_image.save(file.name, file)
    user.save()
    return 200, {"message": "Profile image updated"}


def get_profile(request):
    return request.auth


def change_password(request, data: PasswordChangeSchema):
    user = request.auth

    if not user.check_password(data.current_password):
        return 400, {"message": "Current password is incorrect"}

    if data.new_password != data.confirm_password:
        return 400, {"message": "New passwords do not match"}

    user.set_password(data.new_password)
    user.save()

    return 200, {"message": "Password changed successfully"}


def generate_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password


def request_password_reset(request, data: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        return 404, {"message": "User with this email does not exist"}

    reset_token = jwt.encode({
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, settings.SECRET_KEY, algorithm='HS256')

    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    try:
        html_message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'site_name': settings.SITE_NAME
        })

        send_mail(
            subject="Password Reset Request",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message  # HTML version
        )

        return 200, {"message": "Password reset instructions have been sent to your email"}

    except Exception as e:
        print(f"Error sending email: {str(e)}")  # For debugging
        return 500, {"message": "Failed to send password reset email. Please try again later"}


def confirm_password_reset(request, data: PasswordResetConfirmSchema):
    try:
        payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'], email=payload['email'])

        if data.new_password != data.confirm_password:
            return 400, {"message": "Passwords do not match"}

        user.set_password(data.new_password)
        user.save()

        return 200, {"message": "Password reset successfully"}

    except jwt.ExpiredSignatureError:
        return 400, {"message": "Reset link has expired. Please request a new one."}

    except (jwt.JWTError, User.DoesNotExist):
        return 400, {"message": "Invalid reset link"}