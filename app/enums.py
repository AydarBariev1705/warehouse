from enum import Enum


class OrderStatus(Enum):
    in_progress = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"
