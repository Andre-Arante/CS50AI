from pagerank import *

test_dict = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
damping_factor = 0.85

# Test transition model
# print(transition_model(crawl(sys.argv[1]),"1.html", 0.85))
# print(transition_model(test_dict, '1.html', 0.85))


# print(sample_pagerank(crawl(sys.argv[1]), damping_factor, 10000))
# print(sample_pagerank(test_dict, damping_factor, 10000))

# random_page = random.choice(list(test_dict.keys()))
# model = transition_model(test_dict, random_page, damping_factor)
# print(random.choices(list(model.keys()), weights=model.values(), k=10))

# Test iteration
print(iterate_pagerank(test_dict, damping_factor))