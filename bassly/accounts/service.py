from bassly.accounts.domain import User


def register_user(data):
    required = ["username", "password", "email", "role"]
    missing = [f for f in required if f not in data]

    if missing:
        return None, f"Missing fields: {', '.join(missing)}"

    if User.objects.filter(email=data["email"]).exists():
        return None, "User with this email already exists"

    user = User.objects.create(
        username=data["username"],
        password=data["password"],
        email=data["email"],
        role=data["role"]
    )

    return user, None


def authenticate_user(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if user.password != password:
        return None

    return user
