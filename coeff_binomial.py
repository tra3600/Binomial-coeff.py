#!/usr/bin/env python3
"""Coefficients binomiaux : calcul, triangle de Pascal et développement de (a + b)^n.

Utilisation en ligne de commande :
    python coeff_binomial.py binomial 5 2        # C(5, 2) = 10
    python coeff_binomial.py ligne 6             # 1 6 15 20 15 6 1
    python coeff_binomial.py triangle 8          # triangle de Pascal illustré
    python coeff_binomial.py developpement 4     # (a + b)^4 développé
    python coeff_binomial.py test                # exécute les auto-tests
"""

import argparse
import sys
from typing import List


def _verifier_entier(valeur: int, nom: str) -> None:
    if isinstance(valeur, bool) or not isinstance(valeur, int):
        raise TypeError(f"{nom} doit être un entier, reçu : {valeur!r}")
    if valeur < 0:
        raise ValueError(f"{nom} doit être positif ou nul, reçu : {valeur}")


def fact(p: int) -> int:
    """Retourne la factorielle p! d'un entier p >= 0."""
    _verifier_entier(p, "p")
    resultat = 1
    for i in range(2, p + 1):
        resultat *= i
    return resultat


def binomial(n: int, k: int) -> int:
    """Retourne le coefficient binomial C(n, k) ("k parmi n").

    Calculé de façon multiplicative (sans factorielles géantes) :
    C(n, k) = prod_{i=1..k} (n - k + i) / i, chaque division étant exacte.
    Retourne 0 si k > n.
    """
    _verifier_entier(n, "n")
    _verifier_entier(k, "k")
    if k > n:
        return 0
    k = min(k, n - k)  # symétrie C(n, k) = C(n, n - k)
    resultat = 1
    for i in range(1, k + 1):
        resultat = resultat * (n - k + i) // i
    return resultat


def binomiaux(n: int) -> List[int]:
    """Retourne la liste [C(n, 0), ..., C(n, n)] (ligne n du triangle de Pascal)."""
    _verifier_entier(n, "n")
    ligne = [1]
    for k in range(n):  # C(n, k+1) = C(n, k) * (n - k) / (k + 1)
        ligne.append(ligne[-1] * (n - k) // (k + 1))
    return ligne


def triangle_pascal(n: int) -> List[List[int]]:
    """Retourne les lignes 0 à n du triangle de Pascal (somme de deux voisins)."""
    _verifier_entier(n, "n")
    lignes = [[1]]
    for _ in range(n):
        prec = lignes[-1]
        lignes.append([1] + [a + b for a, b in zip(prec, prec[1:])] + [1])
    return lignes


def afficher_triangle(n: int) -> str:
    """Retourne le triangle de Pascal (lignes 0..n) sous forme de texte centré."""
    lignes = triangle_pascal(n)
    largeur = max(len(str(x)) for x in lignes[-1]) + 1
    largeur += largeur % 2  # largeur paire : décalage d'une demi-cellule exact
    return "\n".join(
        " " * ((n - i) * largeur // 2) + "".join(str(x).center(largeur) for x in ligne).rstrip()
        for i, ligne in enumerate(lignes)
    )


_EXPOSANTS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _terme(var: str, exposant: int) -> str:
    if exposant == 0:
        return ""
    if exposant == 1:
        return var
    return var + str(exposant).translate(_EXPOSANTS)


def developpement(n: int, a: str = "a", b: str = "b") -> str:
    """Retourne le développement de (a + b)^n par la formule du binôme de Newton."""
    _verifier_entier(n, "n")
    termes = []
    for k, c in enumerate(binomiaux(n)):
        facteurs = _terme(a, n - k) + _terme(b, k)
        termes.append(facteurs if c == 1 and facteurs else f"{c}{facteurs}")
    return " + ".join(termes)


def _tests() -> None:
    """Auto-tests rapides (python coeff_binomial.py test)."""
    from math import comb, factorial

    assert fact(0) == 1 and fact(5) == 120
    for n in range(0, 40):
        assert fact(n) == factorial(n)
        assert binomiaux(n) == [comb(n, k) for k in range(n + 1)]
        assert triangle_pascal(n)[-1] == binomiaux(n)
        assert sum(binomiaux(n)) == 2 ** n
        for k in range(0, n + 3):
            assert binomial(n, k) == comb(n, k)
    assert binomial(5, 2) == 10 and binomial(6, 3) == 20 and binomial(3, 5) == 0
    assert binomial(1000, 500) == comb(1000, 500)
    assert developpement(3) == "a³ + 3a²b + 3ab² + b³"
    assert developpement(0) == "1"
    for mauvais in (-1, 2.5, "3", True):
        for f in (fact, binomiaux, triangle_pascal):
            try:
                f(mauvais)
            except (TypeError, ValueError):
                pass
            else:
                raise AssertionError(f"{f.__name__}({mauvais!r}) aurait dû échouer")
    print("Tous les tests sont passés.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Coefficients binomiaux.")
    sous = parser.add_subparsers(dest="commande", required=True)
    p = sous.add_parser("binomial", help="calcule C(n, k)")
    p.add_argument("n", type=int)
    p.add_argument("k", type=int)
    for nom, aide in (("ligne", "ligne n du triangle de Pascal"),
                      ("triangle", "triangle de Pascal jusqu'à la ligne n"),
                      ("developpement", "développe (a + b)^n")):
        p = sous.add_parser(nom, help=aide)
        p.add_argument("n", type=int)
    sous.add_parser("test", help="exécute les auto-tests")

    args = parser.parse_args(argv)
    try:
        if args.commande == "binomial":
            print(f"C({args.n}, {args.k}) = {binomial(args.n, args.k)}")
        elif args.commande == "ligne":
            print(*binomiaux(args.n))
        elif args.commande == "triangle":
            print(afficher_triangle(args.n))
        elif args.commande == "developpement":
            exp = str(args.n).translate(_EXPOSANTS)
            print(f"(a + b){exp} = {developpement(args.n)}")
        else:
            _tests()
    except (TypeError, ValueError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
