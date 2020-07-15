import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000


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

    number_of_pages = len(corpus.keys()) 
    list_of_pages = set(corpus.keys())
    if corpus[page] == set():
        distribution = {}
        for link in list_of_pages:
            distribution[link] = 1 / number_of_pages
        return distribution

    '''

    '''

    distribution = {}
    for link in list_of_pages:
        distribution[link] = (1 - damping_factor) / number_of_pages

    number_of_links = len(corpus[page])
    for link in corpus[page]:
        distribution[link] += damping_factor / number_of_links
    
    return distribution





def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """



    random_range = random.randint(0,len(corpus.keys()) - 1)
    new_page = list(corpus.keys())[random_range]

    count = 0
    results = {}
    for i in corpus.keys():
        results[i] = 0

    while count < n:
        count += 1
        results[new_page] += 1
        distribution = transition_model(corpus, new_page, damping_factor)
        random_num = random.random()
        for page in distribution:
            if distribution[page] > random_num:
                new_page = page
                break
            else:
                random_num -= distribution[page]

    total = sum(results.values())
    for count in results.keys():
        results[count] = results[count] / total

    return results


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranks = {}
    for i in corpus.keys():
        ranks[i] = 1 / len(corpus.keys())
    
    while True:
        tranks = {}

        for page in corpus.keys():
            tranks[page] = (1 - damping_factor) / len(corpus.keys())

            for i, link in corpus.items():
                if page in link:
                    tranks[page] += damping_factor * ranks[i] / len(link)



        count = 0
        for i in ranks.keys():
            if abs(ranks[i] - tranks[i]) < 0.001:
                count += 1
        if count == len(corpus.keys()):
            break

        for i in ranks.keys():
            ranks[i] = tranks[i]

    return ranks
        
if __name__ == "__main__":
    main()
