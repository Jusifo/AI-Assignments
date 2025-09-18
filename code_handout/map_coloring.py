# The map coloring problem from the text book.
# The CSP.backtrack() method needs to be implemented

from csp import CSP, alldiff

variables = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
csp = CSP(
    variables=variables,
    domains={variable: {'red', 'green', 'blue'} for variable in variables},
    edges=[
        ('SA', 'WA'),
        ('SA', 'NT'),
        ('SA', 'Q'),
        ('SA', 'NSW'),
        ('SA', 'V'),
        ('WA', 'NT'),
        ('NT', 'Q'),
        ('Q', 'NSW'),
        ('NSW', 'V'),
    ],
)

print(f"Result: {csp.backtracking_search()}")

print(f"\nBacktracking Calls: {csp.backtracking_calls}\n")

# Example output after implementing csp.backtracking_search():
# {'WA': 'red', 'NT': 'green', 'Q': 'red', 'NSW': 'green', 'V': 'red', 'SA': 'blue', 'T': 'red'}
