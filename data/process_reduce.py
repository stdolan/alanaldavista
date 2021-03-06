#!/usr/bin/env python
import sys
import re
import operator


MAX_ITERATIONS = 15
get_data_regex = re.compile('(\d+),(\d*.\d*)(.*)')


def compute_min(top_20):
    """compute_min takes a min_node string and a dictionary of the PageRanks of
    the current top 20 nodes."""

    min_pagerank = None
    min_node = None

    for node, pagerank in top_20.iteritems():
        if min_pagerank is None:
            min_node = node
            min_pagerank = pagerank
        elif pagerank < min_pagerank:
            min_node = node
            min_pagerank = pagerank

    return min_node, min_pagerank


top_20 = {}

for line in sys.stdin:
    (node, value) = line.split('\t')

    (iteration, score, rest) = get_data_regex.match(value).groups()
    iteration = int(iteration)
    score = float(score)
    # Get iterations.

    # End computation.
    if iteration == 15:
        if len(top_20) < 20:
            top_20[node] = score
        else:
            min_node, min_pagerank = compute_min(top_20)
            if top_20[min_node] < score:
                del top_20[min_node]
                top_20[node] = score
    # Keep iterating.
    else:
        # rest_of_data already has newline.
        sys.stdout.write('NodeId:%s,%d\t%f,%s\n' % (node, iteration, score, rest[1:]))

# If we're done.
if top_20:
    top_20_sorted = sorted(top_20.items(), key=operator.itemgetter(1), reverse=True)
    for node, pagerank in top_20_sorted:
        sys.stdout.write('FinalRank:%f\t%s\n' % (pagerank, node))
