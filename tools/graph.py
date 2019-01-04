#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import logging
from io import open
from time import time
from six.moves import range, zip, zip_longest
from six import iterkeys
from collections import defaultdict, Iterable
import random
from itertools import product,permutations
from scipy.io import loadmat
from scipy.sparse import issparse
from .dijkstra import dijkstra


logger = logging.getLogger("deepwalk")


__author__ = "Bryan Perozzi"
__email__ = "bperozzi@cs.stonybrook.edu"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"

class Graph(defaultdict):
  """Efficient basic implementation of nx `Graph' â€“ Undirected graphs with self loops"""
  def __init__(self):
    super(Graph, self).__init__(list)

  def nodes(self):
    return self.keys()

  def adjacency_iter(self):
    return self.iteritems()

  def subgraph(self, nodes={}):
    subgraph = Graph()

    for n in nodes:
      if n in self:
        subgraph[n] = [x for x in self[n] if x in nodes]

    return subgraph

  def make_undirected(self):

    t0 = time()

    for v in self.keys():
      for other in self[v]:
        if v != other:
          self[other].append(v)

    t1 = time()
    logger.info('make_directed: added missing edges {}s'.format(t1-t0))

    self.make_consistent()
    return self

  def make_consistent(self):
    t0 = time()
    for k in iterkeys(self):
      self[k] = list(sorted(set(self[k])))

    t1 = time()
    logger.info('make_consistent: made consistent in {}s'.format(t1-t0))

    self.remove_self_loops()

    return self

  def remove_self_loops(self):

    removed = 0
    t0 = time()

    for x in self:
      if x in self[x]:
        self[x].remove(x)
        removed += 1

    t1 = time()

    logger.info('remove_self_loops: removed {} loops in {}s'.format(removed, (t1-t0)))
    return self

  def check_self_loops(self):
    for x in self:
      for y in self[x]:
        if x == y:
          return True

    return False

  def has_edge(self, v1, v2):
    if v2 in self[v1] or v1 in self[v2]:
      return True
    return False

  def degree(self, nodes=None):
    if isinstance(nodes, Iterable):
      return {v:len(self[v]) for v in nodes}
    else:
      return len(self[nodes])

  def order(self):
    "Returns the number of nodes in the graph"
    return len(self)

  def number_of_edges(self):
    "Returns the number of nodes in the graph"
    return sum([self.degree(x) for x in self.keys()])/2

  def number_of_nodes(self):
    "Returns the number of nodes in the graph"
    return order()

  def random_walk(self, path_length, alpha=0, rand=random.Random(), start=None):
    """ Returns a truncated random walk.

        path_length: Length of the random walk.
        alpha: probability of restarts.
        start: the start node of the random walk.
    """
    G = self
    if start:
      path = [start]
    else:
      # Sampling is uniform w.r.t V, and not w.r.t E
      path = [rand.choice(list(G.keys()))]

    while len(path) < path_length:
      cur = path[-1]
      if len(G[cur]) > 0:
        if rand.random() >= alpha:
          path.append(rand.choice(G[cur]))
        else:
          path.append(path[0])
      else:
        break
    return [str(node) for node in path]

  def _get_k_hop_neighborhood(self, id_, k):
    if not hasattr(self, 'k_hop_neighbors'):
      self.k_hop_neighbors = {}
    if k not in self.k_hop_neighbors:
      self.k_hop_neighbors[k] = {}
    if id_ in self.k_hop_neighbors[k]:
      return self.k_hop_neighbors[k][id_]

    neighbors = set()
    visited = set()
    to_visit = set([id_])
    next_to_visit = set()
    i = 0
    while i < k:
      while len(to_visit) != 0:
        visit_id = to_visit.pop()
        visited.add(visit_id)
        for to_id in self[visit_id]:
          if to_id == id_:
            continue
          if to_id in neighbors:
            continue
          neighbors.add(to_id)

          if to_id in to_visit:
            continue
          if to_id not in visited:
            next_to_visit.add(to_id)
      to_visit = next_to_visit.copy()
      i += 1
    self.k_hop_neighbors[k][id_] = neighbors
    return neighbors

  def init_shortest_path(self):
    self.shortest_path = {}
    for from_node in self:
      self.shortest_path[from_node] = {}
      for to_node in self[from_node]:
        self.shortest_path[from_node][to_node] = {'path': [to_node], 'cost': 1}

  def init_shortest_path_v2(self):
    self.shortest_path = {}
    for from_node in self:
      self.shortest_path[from_node] = {}
      for to_node in self[from_node]:
        self.shortest_path[from_node][to_node] = 1

  def _get_shortest_path(self, end, start=None):


    '''
    build shortest_path matrix
    :return: shortest_path , {from_node_id : {to_node_id : {path : [node_id1, node_id2,...], cost : <int>}}}
    '''

    def get_shortest_path_node(start_shortest_path, processed):
      path_length = float("inf")
      shortest_end = None
      for end in start_shortest_path:
          if end in processed:
            continue
          path_cost = start_shortest_path[end]['cost']
          if path_cost < path_length:
            path_length = path_cost
            shortest_end = end
      return shortest_end

    shortest_path = self.shortest_path
    start_shortest_path = shortest_path[start]
    processed = set()
    to_node = get_shortest_path_node(start_shortest_path, processed)

    while to_node:

      to_node_shortest_path = shortest_path[to_node]
      cost = start_shortest_path[to_node]['cost']
      neighbors = self[to_node]

      for neighbor in neighbors:
        new_cost = cost + to_node_shortest_path[neighbor]['cost']
        if neighbor not in start_shortest_path:
          start_shortest_path[neighbor] = {}
          start_shortest_path[neighbor]['cost'] = new_cost
          start_shortest_path[neighbor]['path'] = start_shortest_path[to_node]['path'] + [neighbor]
        elif start_shortest_path[neighbor]['cost'] > new_cost:
          start_shortest_path[neighbor]['cost'] = new_cost
          start_shortest_path[neighbor]['path'] = start_shortest_path[to_node]['path'] + start_shortest_path[neighbor]['path']

      processed.add(to_node)
      to_node = get_shortest_path_node(start_shortest_path, processed)

    if end in start_shortest_path:
      return [start] + start_shortest_path[end]['path']
    else:
      return []


# TODO add build_walks in here

def build_deepwalk_corpus(G, num_paths, path_length, alpha=0,
                      rand=random.Random(0)):

  nodes = list(G.nodes())
  
  for cnt in range(num_paths):
    rand.shuffle(nodes)
    for node in nodes:
      yield G.random_walk(path_length, rand=rand, alpha=alpha, start=node)
  

def build_deepwalk_corpus_iter(G, num_paths, path_length, alpha=0,
                      rand=random.Random(0)):
  walks = []

  nodes = list(G.nodes())

  for cnt in range(num_paths):
    rand.shuffle(nodes)
    for node in nodes:
      yield G.random_walk(path_length, rand=rand, alpha=alpha, start=node)


def build_shortest_path(G, nodes, num_paths):

  for node in nodes:
    dis, path = dijkstra(G.shortest_path, node)
    visited = set()
    visited.add(node)
    node_walks = []
    find_count = 0            # find 20 times and then return
    while len(node_walks) < num_paths and find_count < 5 * num_paths:
      find_count += 1
      y = random.randint(0, len(nodes) - 1)
      node_y = nodes[y]
      if node_y in visited:
        continue
      if dis[node_y] < float("inf"):
        node_walks.append(path[node_y])
      visited.add(node_y)
    yield node_walks


def clique(size):
    return from_adjlist(permutations(range(1,size+1)))


# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def parse_adjacencylist(f):
  adjlist = []
  for l in f:
    if l and l[0] != "#":
      introw = [int(x) for x in l.strip().split()]
      row = [introw[0]]
      row.extend(set(sorted(introw[1:])))
      adjlist.extend([row])
  
  return adjlist

def parse_adjacencylist_unchecked(f):
  adjlist = []
  for l in f:
    if l and l[0] != "#":
      adjlist.extend([[int(x) for x in l.strip().split()]])
  
  return adjlist

def load_adjacencylist(file_, undirected=False, chunksize=10000, unchecked=True):

  if unchecked:
    parse_func = parse_adjacencylist_unchecked
    convert_func = from_adjlist_unchecked
  else:
    parse_func = parse_adjacencylist
    convert_func = from_adjlist

  adjlist = []

  t0 = time()
  
  total = 0 
  with open(file_) as f:
    for idx, adj_chunk in enumerate(map(parse_func, grouper(int(chunksize), f))):
      adjlist.extend(adj_chunk)
      total += len(adj_chunk)
  
  t1 = time()

  logger.info('Parsed {} edges with {} chunks in {}s'.format(total, idx, t1-t0))

  t0 = time()
  G = convert_func(adjlist)
  t1 = time()

  logger.info('Converted edges to graph in {}s'.format(t1-t0))

  if undirected:
    t0 = time()
    G = G.make_undirected()
    t1 = time()
    logger.info('Made graph undirected in {}s'.format(t1-t0))

  return G 


def load_edgelist(file_, undirected=True):
  G = Graph()
  with open(file_) as f:
    for l in f:
      x, y = l.strip().split()[:2]
      x = int(x)
      y = int(y)
      G[x].append(y)
      if undirected:
        G[y].append(x)

  G.make_consistent()
  G.init_shortest_path_v2()
  return G


def load_matfile(file_, variable_name="network", undirected=True):
  mat_varables = loadmat(file_)
  mat_matrix = mat_varables[variable_name]

  return from_numpy(mat_matrix, undirected)


def from_networkx(G_input, undirected=True):
    G = Graph()

    for idx, x in enumerate(G_input.nodes_iter()):
        for y in iterkeys(G_input[x]):
            G[x].append(y)

    if undirected:
        G.make_undirected()

    return G


def from_numpy(x, undirected=True):
    G = Graph()

    if issparse(x):
        cx = x.tocoo()
        for i,j,v in zip(cx.row, cx.col, cx.data):
            G[i].append(j)
    else:
      raise Exception("Dense matrices not yet supported.")

    if undirected:
        G.make_undirected()

    G.make_consistent()
    return G


def from_adjlist(adjlist):
    G = Graph()
    
    for row in adjlist:
        node = row[0]
        neighbors = row[1:]
        G[node] = list(sorted(set(neighbors)))

    return G


def from_adjlist_unchecked(adjlist):
    G = Graph()
    
    for row in adjlist:
        node = row[0]
        neighbors = row[1:]
        G[node] = neighbors

    return G


