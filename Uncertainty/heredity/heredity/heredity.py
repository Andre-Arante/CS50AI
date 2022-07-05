import csv
import itertools
import sys
import random

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
    
    joint = 1

    # For each person
    for person in people:

        prob = 1
        pgenes = (2 if person in two_genes else 1 if person in one_gene else 0 )

        # Get their parents
        father = people[person]['father']
        mother = people[person]['mother']
        parents = {father: 0, mother: 0}

        # If parents exist, get the probability for each parent passing on a gene
        if not father and mother:
            # For each parent, calculate the chance that the gene is passed down
            for parent in parents:
                # If parents don't have the gene, then chance of passing on is chance of mutation
                if parent not in one_gene and parent not in two_genes:
                    parents[parent] *= PROBS["mutation"]
                
                # 1 - chance of mutation / 2 gives us the probability of a single gene being passed on
                # If parents have one gene
                elif parent in one_gene:
                    parents[parent] *= 0.5
                # If parents have two genes
                elif parent in two_genes:
                    parents[parent] *= 1 - PROBS["mutation"]

            # If person has 2 genes, probability of father AND mother
            if pgenes == 2:
                prob *= parents[father] * parents[mother]
            # If person has 1 gene, probability of father AND NOT mother OR NOT father AND mother
            elif pgenes == 1:
                prob *= (1 - parents[mother]) * parents[father] + parents[mother] * (1 - parents[father])
            # If person has 0 genes, probability of NOT father AND NOT mother
            else:
                prob *= (1 - parents[father]) * (1 - parents[mother])

        # If no parents, we have to calculate probability based on the PROBS dist
        else:
            prob *= PROBS["gene"][pgenes]

        # Calculate the chance that person has trait already
        prob *= PROBS['trait'][pgenes][person in have_trait]

        joint *= prob

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        pgenes = (2 if person in two_genes else 1 if person in one_gene else 0 )
        ptrait = person in have_trait

        probabilities[person]['gene'][pgenes] += p
        probabilities[person]['trait'][ptrait] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        genes = probabilities[person]["gene"]
        traits = probabilities[person]['trait']

        probabilities[person]["gene"] = {gene: (prob / sum(genes.values())) for gene, prob in genes.items()}
        probabilities[person]["trait"] = {trait: (prob / sum(traits.values())) for trait, prob in traits.items()}


        


if __name__ == "__main__":
    main()
