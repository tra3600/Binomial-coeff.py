def fact(p: int) -> int:
    """
    Calcule la factorielle de p.
    
    Paramètres:
    p (int): Un entier positif.
    
    Retourne:
    int: La valeur de p!.
    """
    if p == 0:
        return 1
    result = 1
    for i in range(1, p + 1):
        result *= i
    return result

# Exemple d'utilisation
print(fact(5))  # Devrait afficher 120
print(fact(0))  # Devrait afficher 1


def binomial(n: int, k: int) -> int:
    """
    Calcule le coefficient binomial C(n, k).
    
    Paramètres:
    n (int): Un entier positif.
    k (int): Un entier positif tel que k <= n.
    
    Retourne:
    int: La valeur du coefficient binomial.
    """
    return fact(n) // (fact(k) * fact(n - k))

# Exemple d'utilisation
print(binomial(5, 2))  # Devrait afficher 10
print(binomial(6, 3))  # Devrait afficher 20


def binomiaux(n: int):
    """
    Affiche tous les coefficients binomiaux C(n, k) pour k = 0, 1, 2, ..., n.
    
    Paramètres:
    n (int): Un entier positif.
    """
    coefficients = [binomial(n, k) for k in range(n + 1)]
    print(', '.join(map(str, coefficients)))

# Exemple d'utilisation
binomiaux(6)  # Devrait afficher 1, 6, 15, 20, 15, 6, 1