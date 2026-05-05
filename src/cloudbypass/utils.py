def convert_bytes(value, end_unit="Y"):
    if not value:
        return "0"
    units = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    if len(end_unit) == 1:
        end_unit = end_unit.upper()
    end_idx = units.index(end_unit)
    unit = 0
    value = float(value)
    while value >= 1024:
        value /= 1024
        unit += 1
        if unit == end_idx:
            break
    return f"{value:.2f} {units[unit]}B"
