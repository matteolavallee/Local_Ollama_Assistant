# Fonctions calculatoires
import math

def add_two_numbers(a: float, b: float) -> float:
  """
  Additionne deux nombres.

  Args:
    a: Le premier nombre.
    b: Le deuxième nombre.

  Returns:
    La somme des deux nombres.
  """
  print(f"--- Exécution de la fonction: add_two_numbers(a={a}, b={b}) ---\n")
  return a + b

def sqrt(x: float) -> float:
  """
  Calcule la racine carrée d'un nombre.

  Args:
    x: Le nombre dont on veut la racine carrée. Doit être non-négatif.

  Returns:
    La racine carrée de x.
  """
  print(f"--- Exécution de la fonction: sqrt(x={x}) ---\n")
  return math.sqrt(x)

def factorial(n: int) -> int:
  """
  Calcule la factorielle d'un nombre entier.

  Args:
    n: Un entier non-négatif.

  Returns:
    La factorielle de n.
  """
  print(f"--- Exécution de la fonction: factorial(n={n}) ---\n")
  return math.factorial(n)

def pow(x: float, y: float) -> float:
  """
  Élève un nombre (x) à une puissance (y).

  Args:
    x: Le nombre de base.
    y: L'exposant.

  Returns:
    Le résultat de x élevé à la puissance y.
  """
  print(f"--- Exécution de la fonction: pow(x={x}, y={y}) ---\n")
  return math.pow(x, y)


# On expose maintenant nos propres fonctions wrapper qui, elles, appellent les fonctions math.
# Cela garantit qu'elles acceptent toutes des arguments par mot-clé.
tools = [
    add_two_numbers,
    sqrt,
    factorial,
    pow,
]

available_functions = {
    "add_two_numbers": add_two_numbers,
    'sqrt': sqrt,
    'factorial': factorial,
    'pow': pow,
}