import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):            
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def fn_prob_with_parents(person, people, one_gene, two_genes, child_copies):
    """
    return: Probability of child have cero, one or two genes
            based on their fathers.
            -   i.e.: What’s the probability that Harry has 1 copy of the gene?
    """
    p_mutate = PROBS["mutation"]
    p_NO_mutate = 1 - p_mutate

    prob_pass_parents = {"father":{}, "mother":{}}
    for parent in prob_pass_parents:

        if people[person][parent] in one_gene:
            prob_pass = 0.5
        elif people[person][parent] in two_genes:
            # prob_pass = 1 - PROBS["mutation"]
            prob_pass = 1
        else:
            # prob_pass = PROBS["mutation"]
            prob_pass = 0

        prob_pass_NO_mutate = prob_pass * p_NO_mutate
        prob_pass_mutate = prob_pass * p_mutate
        prob_NO_pass_mutate = (1-prob_pass) * p_mutate
        prob_NO_pass_NO_mutate = (1-prob_pass) * p_NO_mutate

        prob_pass_parents[parent]["prob_pass_NO_mutate"] = prob_pass_NO_mutate
        prob_pass_parents[parent]["prob_pass_mutate"] = prob_pass_mutate
        prob_pass_parents[parent]["prob_NO_pass_mutate"] = prob_NO_pass_mutate
        prob_pass_parents[parent]["prob_NO_pass_NO_mutate"] = prob_NO_pass_NO_mutate
    
    if child_copies == 1:
        prob = (
            (prob_pass_parents["father"]["prob_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_pass_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_pass_mutate"] * prob_pass_parents["mother"]["prob_pass_NO_mutate"]) + \
            # 0 + \
            (prob_pass_parents["father"]["prob_NO_pass_mutate"] * prob_pass_parents["mother"]["prob_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_mutate"])
        )
    elif child_copies == 2:
        prob = (
            (prob_pass_parents["father"]["prob_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_mutate"] * prob_pass_parents["mother"]["prob_pass_NO_mutate"])
        )
    else:
        prob = (
            (prob_pass_parents["father"]["prob_pass_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_NO_mutate"]) + \
            (prob_pass_parents["father"]["prob_pass_mutate"] * prob_pass_parents["mother"]["prob_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_pass_mutate"]) + \
            (prob_pass_parents["father"]["prob_NO_pass_NO_mutate"] * prob_pass_parents["mother"]["prob_NO_pass_NO_mutate"])
        )

    # print("\n________________________\t fn_prob_with_parents")
    # print(prob_pass_parents, two_genes)
    return prob
 

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # print("\n________________________\tjoint_probability")
    # print(people)

    joint_prob = 1

    # People contains everything
    # So, I check each single person, 1 by 1
    for person in people:
        # print(person)

        # check how many gene copies has this person
        num_copies = 0
        if person in one_gene:      num_copies = 1
        elif person in two_genes:   num_copies = 2

        trait = False
        if person in have_trait:    trait = True

        # check if this person has not parents
        # i.e.: prob of JAMES has 0 genes and has trait. James is like Batman 
        prob_without_parents = 1
        prob_with_parents = 1

        if people[person]['mother'] is None or people[person]['father'] is None:
            # Remenber this is = prob_having_gene * prob_having_trait
            prob_without_parents = PROBS["gene"][num_copies] * PROBS["trait"][num_copies][trait]
            joint_prob *= prob_without_parents
        else:
            # Remenber this is = prob_having_gene * prob_having_trait
            # print(person, num_copies)
            prob_with_parents = (fn_prob_with_parents(person, people, one_gene, two_genes, num_copies) * PROBS["trait"][num_copies][trait])
            joint_prob *= prob_with_parents

    # print("\n\n", joint_prob)
    return joint_prob
    # raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # print("\n________________________\t update")
    # print(probabilities)

    for person in probabilities:
        # print(person)

        # check how many gene copies has this person
        num_copies = 0
        if person in one_gene:      num_copies = 1
        elif person in two_genes:   num_copies = 2

        trait = False
        if person in have_trait:    trait = True

        probabilities[person]["gene"][num_copies] += p
        probabilities[person]["trait"][trait] += p

    # print(probabilities)
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        sum_probs_genes = sum(probabilities[person]["gene"].values())
        sum_probs_traits = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] / sum_probs_genes
        
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] / sum_probs_traits
    # raise NotImplementedError


if __name__ == "__main__":
    main()
