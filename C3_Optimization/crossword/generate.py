import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # print("\n")
        # print(self.domains)
        # print("\n")

        for v in self.domains:
            # print(v, type(v))
            for word in set(self.domains[v]):
                # print(word)
                if len(word) != v.length:
                    self.domains[v].remove(word)

        # print(self.domains) 
        # print("\n\n")
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # print("\n", "\t BEFORE", self.domains[x])
        # print("", "\t Contra", self.domains[y])

        overlap = self.crossword.overlaps[x, y]
        # print("\n", "\t", overlap, type(overlap))

        revised = False
        if overlap is None: return revised
        
        i, j = overlap
        # print("\n", "\t", i, j)

        for word_X in set(self.domains[x]):
            same_value = False
            for word_Y in set(self.domains[y]):
                if word_X[i] == word_Y[j]:
                    same_value = True
                    break
            
            if same_value == False:
                self.domains[x].remove(word_X)
                # print(" AFTER", "\t", self.domains[x])
                revised =  True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # self.revise(Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3))

        if arcs is None:
            arcs = []

            for varX in self.domains:
                for varY in self.domains:
                    if varX != varY and self.crossword.overlaps[varX, varY]:# and ((varY, varX) not in arcs):
                        arcs.append((varX, varY))

        # print("\n ac3_1 \t", self.domains, "\t")
        # print("\n ac3_1 \t", arcs)
        while arcs:
            # for arc in arcs:
            #     # print("\n", "\t", arc[0], "\n", type(arc))
            #     arcs.remove(arc)
            arc = arcs.pop(0)

            # print("\n ac3_2X \t", self.domains[arc[0]], "\t", arc[0])
            # print(" ac3_2Y \t", self.domains[arc[1]], "\t", arc[1])

            if self.revise(arc[0], arc[1]):
                if not self.domains[arc[0]]: # if size of X.domain == 0:
                    return False
                
                # print("\n ac3_2.2A \t", self.crossword.neighbors(arc[0]))
                # print(" ac3_2.2B \t", arc[0])
                # print(" ac3_2.2C \t", arc[1])

                for z in self.crossword.neighbors(arc[0]):
                    if z != arc[1]:
                        arcs.append((z, arc[0]))

            # print("\n ac3_2X2 \t", self.domains[arc[0]])
            # print(" ac3_2Y2 \t", self.domains[arc[1]])

        # print("\n ac3_3 \t", self.domains, "\t")
        return True
                    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # print("\n assignment_complete \t", "\t")
        for var in self.crossword.variables:
            # print(" \t", self.crossword.neighbors(var), "\t")
            # print(" \t", self.domains[var], "\t")
            if var not in assignment: return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            word = assignment[var]

            if len(word) != var.length:
                return False
            
            for remaining_var in assignment:
                if remaining_var != var:
                    if word == assignment[remaining_var]:
                        return False
                    
            for neig in self.crossword.neighbors(var):
                if neig in assignment:
                    var_dig, neig_dig = self.crossword.overlaps[var, neig]
                    neig_word = assignment[neig]

                    if word[var_dig] != neig_word[neig_dig]: 
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        unmatches =[]
        for word in self.domains[var]:
            n_unmatches = 0

            for neig in self.crossword.neighbors(var):

                if neig not in assignment:
                    overlap = self.crossword.overlaps[var, neig]

                    if overlap:
                        word_dig, neig_dig = overlap

                    for neig_word in self.domains[neig]:
                        if word[word_dig] != neig_word[neig_dig]:
                            n_unmatches = n_unmatches + 1

            unmatches.append((word, n_unmatches))
        unmatches.sort(key=lambda x:x[1])
        return [word for word, _ in unmatches]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        final_var = None
        min_remng_val = float("inf")
        high_deg = float("-inf")

        for var in self.crossword.variables:
            if var not in assignment:
                n_remng_val = len(self.domains[var])
                n_degrees = len(self.crossword.neighbors(var)) 

                if n_remng_val < min_remng_val:
                    final_var = var
                    min_remng_val = n_remng_val
                    high_deg = n_degrees

                elif n_remng_val == min_remng_val:
                    if n_degrees > high_deg:
                        final_var = var
                        high_deg = n_degrees

        return final_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                new_assignment = assignment.copy()
                new_assignment[var] = value

                if self.consistent(new_assignment):
                    result = self.backtrack(new_assignment)
                    if result is not None: return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
