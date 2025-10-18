def calculate_total_price(booking):
    total = 0
    for sb in booking.service_bookings.all():
        total += sb.get_total()
    return total
