import numpy as np
import oineus as oin
f = np.random.randn(16, 16, 16)
params = oin.ReductionParams()
params.n_threads = 2
dgms = oin.compute_diagrams_ls(data=f, negate=False, wrap=False, params=params, include_inf_points=True, max_dim=2)
dgm = dgms.in_dimension(0)
