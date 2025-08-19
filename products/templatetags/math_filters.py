from django import template

register = template.Library()

@register.filter
def divided_by(value, divisor):
    """تقسیم عدد بر عدد دیگر (با رند کردن به بالا اگر نیاز بود)"""
    try:
        value = int(value)
        divisor = int(divisor)
        return (value + divisor - 1) // divisor  # برای اینکه رند بالا باشه
    except (ValueError, ZeroDivisionError):
        return None
