from icecream import ic
import oineus as oin
import numpy as np
import matplotlib.pyplot as plt
DIM = 1
WASS_DIST_Q = 2
max_dim = 1
empty = oin.Diagrams_double(DIM+1)[DIM]
Z = np.random.random((100,2))
fil,longest_edges = oin.get_vr_filtration_and_critical_edges(Z, max_dim=2, max_radius=np.inf, n_threads=4)
top_opt = oin.TopologyOptimizer(fil)
diagram = top_opt.compute_diagram(include_inf_points=False)
#Same loss as before with edges, i.e. align edges to their critical lengths
indices, values = top_opt.match(empty, DIM, WASS_DIST_Q )
ic(indices,values)
