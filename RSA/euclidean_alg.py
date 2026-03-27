# Author: unknown

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Erweiterter euklidischer Algorithmus.
    
    Findet x und y, sodass: a*x + b*y = gcd(a, b)
    
    Args:
        a: Erste ganze Zahl
        b: Zweite ganze Zahl
        
    Returns:
        Tupel (gcd, x, y) wobei gcd = gcd(a, b) und a*x + b*y = gcd
    """
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y


def get_modular_inverse(a: int, mod: int) -> int:
    """
    Berechnet die modulare Inverse von a modulo mod.
    
    Findet x, sodass: a*x ≡ 1 (mod mod)
    
    Args:
        a: Die Zahl, deren modulare Inverse gesucht wird
        mod: Der Modulus
        
    Returns:
        Die modulare Inverse von a modulo mod (im Bereich [0, mod))
        
    Raises:
        ValueError: Wenn gcd(a, mod) != 1 (keine Inverse existiert)
    """
    gcd, x, _ = extended_gcd(a, mod)
    
    if gcd != 1:
        raise ValueError(f"Modulare Inverse existiert nicht: gcd({a}, {mod}) = {gcd} != 1")
    
    # Stelle sicher, dass das Ergebnis im Bereich [0, mod) liegt
    return x % mod

