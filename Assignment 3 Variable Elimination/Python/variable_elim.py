"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
import pandas as pd

class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def create_product_formula(self):
        product_formula = []
        for variable, index in enumerate(self.network.nodes):
            if index == 0:
                product_formula.append(variable)
                continue
            else:
                product_formula.append({variable: [conditional for conditional in self.network.nodes[0, index]]})
        return product_formula
    def reduce_product_formula(self, product_formula):
        for probability in product_formula:
            for variable, condition in probability.items():
                if condition not in self.network.parents[variable]:
                    probability.pop(condition)
        return product_formula

    def reduce_factor(self, factor, observed_variable):
        factor.drop(factor[factor == observed_variable.values()].index, inplace=True)

    def multiply_factors(self, factor1, factor2):
        factor1.merge(factor2, how='outer', left_index=True, right_index=True)

    def sum_out_variable(self, factor, variable):
        factor.groupby(by=[variable], axis=1).sum()


    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        # Variable elimination algorithm outline:
        # Find the query variable (given as input query)
        # Find the observed variable(s) (given as input observed)


        # Write down the product formula to compute the query
            # The probability distribution of the query variable is given by the sum of all other variables in the network of their joint probability distribution
            # This is the same as the sum of all other variables and the p(A) * p(B | A) * p(C | A,B) * p(D | A,B,C), etc.
        product = self.create_product_formula()


        # Write down the reduced formula based on the network structure
        reduced_product = self.reduce_product_formula(product)
            # look for edges between variables, If you need to compute p(D | A,B,C), but there is no edge between A and D, then you can reduce this to p(D | B,C)

        # Find factors and reduce observed variables
        for observed_variable in observed.keys():
            for factor in reduced_product:
                if observed_variable in factor.items():
                    self.reduce_factor(factor, observed_variable)

            # look at your sum from previous again, a factor is just one part of the sum/product:
            # for example f0(A) (the first factor, the first item in the sum) = {a: 0.9, -a: 0.1} so here it is just the probability of all values of A
            # These factors are tables!!

            # If there are observed variables, for example; A is observed to be True, then you can remove all table rows where a=False

        # Fix an elimination ordering (already given as input elim-order)
            # some notes: the query variable can never be in the elim-order
            # Best practice to take a leaf variable (a variable without outgoing edges, so only incoming)
            # This is just a list of variables

        # For every variable Z in this elim-order:
        for variable_z in elim_order:

            # Multiply all (YES ALL) factors containing Z:
            self.multiply_factors(reduced_product, variable_z)

                # look at every value in one factor that is contained in the other factor and simply multiply the probabilities
                # An entry in f0(A) could be a: 0.9 and in f3(A,B,C) a,b,c: 0.1 then a,b,c becomes 0.9*0.1 = 0.09
                # then with the product of factors (the table) you sum out a variable

            # Sum out Z to obtain a new factor fz
            self.sum_out_variable(reduced_product, variable_z)
                # for example variable Z = D, then all factors containing D for example is  f3(B,D) = {bd: 0.1, b-d: 0.9, -bd: 0.8, -b-d, 0.2}
                # Then new factor is created fn(B) = {b: 1, -b: 1} (just add b+b and -b + -b (- is not) from the table)

            # Remove the multiplied or old factors from the list and add fz
                # The result should be one or more factors only containing the query variables
                # If there are multiple factors, you should still multiply the factors.

        # Normalize the result to make it a probability distribution
            # How? divide the factor by the marginalization of the factor
        