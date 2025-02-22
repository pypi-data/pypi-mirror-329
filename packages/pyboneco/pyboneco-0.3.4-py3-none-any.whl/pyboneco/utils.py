def build_software_version(high: int, low: int) -> str:
    return f"{(high >> 4) & 15}.{high & 15}{(low >> 4) & 15}{low & 15}"
