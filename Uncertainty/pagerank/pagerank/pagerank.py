import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = {}

    pages = corpus.keys()
    N = len(corpus)
    links = corpus[page]

    for p in pages:
        
        # First way surfer can end up on page (surfer just chose at random)
        distribution[p] = (1-damping_factor) / N

        # Second way surfer can end up on page (by following a link from current page)
        if links:
            # If page is linked to, probability is dampning factor (0.85) / the number of links
            # Note: damping factor is used instead of 1 because there is still a chance (0.15) that a page is chosen but not linked to
            if p in links:
                distribution[p] += damping_factor / len(links)
        # If no pages are linked to, then each page has an equal chance of being chosen
        else:
            distribution[p] = 1 / N


    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Set up dictionary entry for each page
    estimated_values = {}
    for page in corpus.keys():
        estimated_values[page] = 0  

    random_page = random.choice(list(corpus.keys()))
    
    for i in range(n):

        model = transition_model(corpus, random_page, damping_factor)
        random_page = random.choices(list(model.keys()), weights=model.values(), k=1)[0]

        estimated_values[random_page] += 1

    return { page: rank / n for page, rank in estimated_values.items() }




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    estimated_values = {}
    diff = 999

    for page in corpus.keys():
        estimated_values[page] = 1 / N 

    dist = sample_pagerank(corpus, damping_factor, 10000)
    while diff > 0.001:
        for page in dist:
            temp = (estimated_values[page] + dist[page]) / 2
            diff = estimated_values[page] - temp
            estimated_values[page] = temp
    return dist

if __name__ == "__main__":
    main()
