import random
from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        #TODO A domain Cache for the last results produced by AC-3
        self.ac3_domains = domains.copy()


        #TODO Added a neighbors dictionary in order to quickly check the neighbors of a node
        self.neighbors = {var: set() for var in self.variables}
        for (var1, var2) in edges:
            self.neighbors[var1].add(var2)
            self.neighbors[var2].add(var1)

        #Should return a dictionary like this:
        #{ 'SA': {'WA', 'NT', 'Q', 'NSW', 'V', 'T'},
        #  'WA': {'NT', 'Q', 'NSW', 'V', 'SA', 'T'},
        #  ...}


        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def revise(self, X1, X2):
        # Underlying construct from AIMA 4th Ed., Global Edition
        for value in list(self.domains[X1]):
            if not any(self.binary_check(X1, value, X2, value2) for value2 in self
                    .domains[X2]):
                 self.ac3_domains[X1].remove(value)
                 return True

            # for d_value in self.domains[X2]:
            #     if self.binary_constraints.keys().__contains__((X1, X2)) and self.binary_constraints[(X1, X2)].__contains__((value, d_value)):
            #         found_partner = True
            #         break
            #     elif self.binary_constraints.keys().__contains__((X2, X1)) and self.binary_constraints[(X2, X1)].__contains__((d_value, value)):
            #         found_partner = True
            #         break
            # if not found_partner:
            #     self.ac3_domains[X1].remove(value)
            #     return True
            # else:
        return False

    def ac_3(self) -> bool:
        # Underlying construct from AIMA 4th Ed., Global Edition

        # Code from
        queue: set[tuple[str, str]] = set()
        for (variable1, variable2) in self.binary_constraints.keys():
            queue.add((variable1, variable2))
            #queue.add((variable2, variable1))

        reference_queue = queue.copy()

        while len(queue):
            (v1, v2) = queue.pop()
            if self.revise(v1, v2):
                if len(self.domains[v1]) == 0:
                    return False
                for (var1, var2) in reference_queue:
                    if var1 == v1 and var2 != v2:
                        queue.add((var2, var1))

        return True

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """


        def backtrack(assignment: dict[str, Any]):

            #Pre assigning values with a domain consisting of only one element
            for key in self.domains.keys():
                if len(self.domains[key]) == 1:
                    assignment[key] = next(iter(self.domains[key]))

            #Running AC-3 once
            #if self.ac_3():
            #    self.domains = self.ac3_domains.copy()

            # Underlying construct from AIMA 4th Ed., Global Edition
            if self.select_unassigned_variable(self.binary_constraints, assignment) == None:
                return assignment
            var = self.select_unassigned_variable(self.binary_constraints, assignment)
            for value in self.order_domain_values(var):
                domain_snapshot = self.domains.copy()
                if self.value_consistency_check(assignment, var, value):
                    assignment[var] = value
                    print(f"Variable: {var} -> Value: {value}")
                    #if self.ac_3():
                    #      self.domains = self.ac3_domains.copy()
                    result = backtrack(assignment)
                    if result:
                        return result
                    self.domains = domain_snapshot.copy()
                    assignment.pop(var)
                    print(f"\n Unassigned var: {var} Value: {value}\n")

            return None
        return backtrack({})
    def value_consistency_check(self, assignment, variable, value):
        partners = self.neighbors[variable]
        partners = list(partners)


        for vari in partners:
            if assignment.keys().__contains__(vari):
                if not self.binary_check(variable, value, vari, assignment[vari]):
                    #print(f"Binary Check failed for {variable} and {vari}")
                    return False
        return True

    def select_unassigned_variable(self, keyset: dict[tuple[str, str], set], assignment: dict[str, Any]):
         for var in self.variables:
            if var not in assignment.keys():
                return var
         return None

    def order_domain_values(self, var: str):
        return self.domains[var]

    def binary_check(self, variable1: str, value1: str, variable2: str, value2: str):
        #Code taken from above
         if (
             (variable1, variable2) in self.binary_constraints and
             (value1, value2) not in self.binary_constraints[(variable1, variable2)]
         ) or (
             (variable2, variable1) in self.binary_constraints and
             (value1, value2) not in self.binary_constraints[(variable2, variable1)]
         ):
             return False
         return True

def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]

