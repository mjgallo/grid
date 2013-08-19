from django.dispatch import Signal


# A founder has invited a potential new user to his grid
user_invited = Signal(providing_args=["to_user", "grid", "request"])

# A user has requested that a founder let him join his grid
grid_requested = Signal(providing_args=["to_founder", "grid", "request"])