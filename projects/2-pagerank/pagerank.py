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
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")


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
    selected_page_links = len(corpus[page])
    distribution_selected_link = (100 / selected_page_links) * damping_factor / 100

    distribution_rest_link = (100 / len(corpus)) * (1 - damping_factor) / 100


    distribution = dict()
    for key in corpus:
        if key in corpus[page]:
            distribution[key] = distribution_selected_link + distribution_rest_link
        else:
            distribution[key] = distribution_rest_link

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_distribution = dict()
    for key in corpus:
        dict_distribution[key] = 0
    initial_page = random.choice(list(corpus.keys()))
    dict_distribution[initial_page] += 1

    for i in range(n-1):
        distribution = transition_model(corpus, initial_page, damping_factor)
        for key in distribution:
            if random.random() < distribution[key]:
                initial_page = key
                dict_distribution[key] += 1
                break
    
    dist_sum = 0
    for key in dict_distribution:
        dict_distribution[key] = dict_distribution[key] / n
        dist_sum += dict_distribution[key]

    for key in dict_distribution:
        dict_distribution[key] = dict_distribution[key] / dist_sum
        distribution_str = "{:.5f}".format(dict_distribution[key])
        dict_distribution[key] = float(distribution_str)

    return dict_distribution


# Corpus {
# '1.html': {'2.html'}, 
# '2.html': {'1.html', '3.html'},
#  '3.html': {'4.html', '2.html'}, 
# '4.html': {'2.html'}}   

# Links 1: 1 0,25 - 0,16
# Links 2: 3 0,75 - 0,5
# Links 3: 1 0,25 - 0,16
# Links 4: 1 0,25 - 0,16
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
