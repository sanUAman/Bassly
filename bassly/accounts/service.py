from bassly.accounts.domain import User


def register_user(data):
    required = ["email", "name", "password"]
    missing = [f for f in required if f not in data]

    if missing:
        return None, f"Missing fields: {', '.join(missing)}"

    if User.objects.filter(email=data["email"]).exists():
        return None, "User with this email already exists"

    user = User.objects.create(
        email=data["email"],
        name=data["name"],
        password=data["password"],
    )

    return user, None


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return None

    if not user.check_password(password):
        return None

    return user
