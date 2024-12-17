import struct

def float_to_ieee754(value):
    """
    Конвертирует число с плавающей точкой в битовое представление IEEE-754 (double, 64 бита).
    Возвращает в виде 16-ричного числа.
    """
    # Используем struct.pack для упаковки float в 8 байт (double) и преобразуем в hex
    packed = struct.pack('>d', value)  # '>d' означает big-endian double
    hex_value = ''.join(f'{byte:02x}' for byte in packed)
    return f"0x{hex_value}"