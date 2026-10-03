# Binomial-coeff.py

Coefficients binomiaux en Python pur (aucune dépendance) : calcul de C(n, k),
lignes et triangle de Pascal, développement de (a + b)ⁿ.

## Utilisation

```
python coeff_binomial.py binomial 5 2      # C(5, 2) = 10
python coeff_binomial.py ligne 6           # 1 6 15 20 15 6 1
python coeff_binomial.py triangle 6        # triangle de Pascal illustré
python coeff_binomial.py developpement 4   # (a + b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴
python coeff_binomial.py test              # auto-tests
```

```
$ python coeff_binomial.py triangle 6
             1
           1   1
         1   2   1
       1   3   3   1
     1   4   6   4   1
   1   5   10  10  5   1
 1   6   15  20  15  6   1
```

## En tant que module

```python
from coeff_binomial import binomial, binomiaux, triangle_pascal, developpement
binomial(6, 3)      # 20
binomiaux(4)        # [1, 4, 6, 4, 1]
developpement(3)    # 'a³ + 3a²b + 3ab² + b³'
```

## Fonctions

- `fact(p)` : factorielle.
- `binomial(n, k)` : C(n, k), calcul multiplicatif exact (rapide même pour n très grand) ; 0 si k > n.
- `binomiaux(n)` : liste des C(n, k), k = 0..n.
- `triangle_pascal(n)` / `afficher_triangle(n)` : lignes 0..n du triangle.
- `developpement(n, a, b)` : formule du binôme de Newton.

Les entrées invalides (négatives, non entières) lèvent `ValueError` / `TypeError`.
