import math


def cursed_toggle(b: bool) -> bool:
    """Toggle the boolean input `b`."""
    if type(b) is not bool:
        raise TypeError("Argument `b` must be Boolean.")

    return bool(_cursed_toggle(b))


def _cursed_toggle(b: bool) -> complex:
    """Implement the core of the cursed_toggle function.

    Main part is excluded for proper testing. Behaviour of the function should be
        f(1) -> 0
        f(0) -> 1
    But with a bool conversion in the return, it would be sufficient that
        f(1) -> 0
        f(0) -> anything but 0
    because bool(5), bool(-2), etc. will result in True.

    """
    return -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> math.factorial(int((-math.e**(1j * math.pi) - math.e**(1j * math.pi) - math.e**(1j * math.pi)).real))) * b
