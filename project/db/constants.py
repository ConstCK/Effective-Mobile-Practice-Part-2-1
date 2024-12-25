import enum

# Класс с перечнем этапов покупки книги


class BuyingStatus(enum.Enum):
    PAYING = 'Оплата'
    PACKING = 'Упаковка'
    DELIVERING = 'Доставка'
    FINISHED = 'Завершено'
