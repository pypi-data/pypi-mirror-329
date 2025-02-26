# Quick introduction to Oineus

## Simplices and Filtrations

```python
import oineus as oin
import numpy as np
import torch
```

First, let us do everything by hand. If we want to create a filtration,
we need to create simplices first. We have a filtration of a triangle:

```python
# vertices
v0 = oin.Simplex([0])
v1 = oin.Simplex([1])
v2 = oin.Simplex([2])

# edges
e1 = oin.Simplex([0, 1])
e2 = oin.Simplex([0, 2])
e3 = oin.Simplex([1, 2])

# triangle
t1 = oin.Simplex([0, 1, 2])
```

Note that we did not specify values.
We now put simplices into a list and create a parallel list
of values, so that simplex `simplices[i]` enters filtration at time `values[i]`.
```python
simplices = [v0,  v1,  v2,  e1,  t1,  e2,  e3]
values =    [0.1, 0.2, 0.3, 1.2, 4.0, 1.4, 2.1]
```
We put simplices of positive dimension in arbitrary order here. 
**Vertices must always appear in the list first, and in the order prescribed by their index**.

Now we create a filtration.
Parameter `keep_ids` is set to `False`, because we did not set ids
of a simplex manually. Parameter `sort` is set to `True`, because
the list `simplices` is not sorted.

```python
# constructor will sort simplices and assign sorted_ids
fil = oin.Filtration(simplices, values)

print(fil)
```

Note that:
1. Each simplex has `id`, which equals its index in the list `simplices`. This is precisely why we insist
that vertex `[i]` appears in the `i`-th position in `simplices`: we want the `id` of a vertex
to match its index we use when we create positive-dimensional simplices: `oin.Simplex([0, 2])`
consists of vertices `simplices[0]` and `simplices[2]`.
2. Each simplex has `sorted_id`, which equals its index in the filtration order.
When we ask `fil` for simplices, they will appear in the order determined
by the `sorted_id`.

Alternatively, we can provide values in each simplex, which
is a more object-oriented way:
```python
v0 = oin.Simplex([0], 0.1)
v1 = oin.Simplex([1], 0.2)
v2 = oin.Simplex([2], 0.3)

e1 = oin.Simplex([0, 1], 1.2)
e2 = oin.Simplex([0, 2], 1.4)
e3 = oin.Simplex([1, 2], 2.1)

t1 = oin.Simplex([0, 1, 2], 4.0)

simplices = [v0,  v1,  v2,  e1,  t1,  e2,  e3]

fil = oin.Filtration(simplices)

print(fil)
```

The constructor of a filtration has some additional arguments:
* `keep_ids` is `False` by default, that is why `id`s are overwritten. Set it to `True` to preserve original `id`s.
Caveat: vertex `i` must still have `id == i` and the `id`s are unique.
* `sort` is `True` by default. If you know that your simplices are already in the correct
order, you can set it to `False`.

## Common filtrations

### Vietoris-Rips. 

You can create a VR filtration from a point cloud or from a distance matrix.


For point cloud, only dimensions 1, 2 and 3 are supported.
An input can be a NumPy array, a Jax array or a PyTorch tensor.
The shape is `(#points, dimension)`, in other words, each point must be a row
in a matrix.

```python
import numpy as np

# create 20 random points in space
np.random.seed(1)
n_points = 20
dim = 3
points = np.random.uniform(size=(n_points, dim))

fil = oin.get_vr_filtration(points=points, max_dim=3, max_radius=2)
print(fil)
```

The parameters are:
* `points`: coordinates of points in the point cloud.
* `max_dim`: the resulting filtration will contain simplices up to and including `max_dim`.
If you want to compute persistence diagrams in dimension `d`, you need `max_dim >= d+1`.
* `max_radius`: only consider balls up to this radius.

For distance matrix:

```python
import numpy as np

# create 20 random points in space
np.random.seed(1)
n_points = 20
dim = 6
points = np.random.uniform(size=(n_points, dim))

fil = oin.get_vr_filtration(distances=distances, max_dim=3, max_radius=2)
print(fil)
```

All arguments to `get_vr_filtration` are keyword-only, to avoid confusion.
In other words, you cannot say 
`oin.get_vr_filtration(x, max_dim=3, max_radius=2)`, because it is unclear whether `x` is a point cloud
or a distance matrix.
Supplying both `points` and `distances` will raise an error.

### Lower-star filtration.

Lower-star filtrations are supported for functions on a regular D-dimensional grid
for D = 1 , 2, or 3. Function values are represented as an D-dimensional NumPy array.

```python
# create scalar function on 8x8x8 grid
f = np.random.uniform(size=(8, 8, 8))

fil = oin.get_freudenthal_filtration(data=f, max_dim=3)
```

If you want upper-star filtration, set `negate` to `True`:
```python
fil = oin.get_freudenthal_filtration(data=f, negate=True, max_dim=3)
```
If you want periodic boundary conditions (D-dimensional torus instead
of D-dimensional cube), set `wrap` to `True`:
```python
fil = oin.get_freudenthal_filtration(data=f, wrap=True, max_dim=3)
```

  
## Persistence Diagrams

Persistence diagram is computed from `R=DV, RU=D` decomposition.
In fact, we only need the `R` matrix to read off the persistence pairing,
but other matrices are needed in topological optimization.
The corresponding class
is called `VRUDecomposition`. When we create it, we must specify whether we want homology
(`dualize=False`) or cohomology (`dualize=True`).

```python
# no cohomology
dualize = False
# create VRU decomposition object, does not perform reduction yet
dcmp = oin.Decomposition(fil, dualize)
```

In order to perform reduction, we need to set parameters.
This is done through a single object of class `ReductionParams` that encapsulates all
of these parameters. 

```python
rp = oin.ReductionParams()
```
Some of the parameters are:
* `rp.clearing_opt` whether you want to use clearing optimization.
* `rp.n_threads`: number of threads to use, default is 1.
* `rp.compute_v`: whether you want to compute the `V` matrix. `True` by default.
* `rp.compute_u`: whether you want to compute the `U` matrix. `False` by default.
This cannot be done in multi-threaded mode, so the reduction will return an error, if `n_threads > 1`
and this option is set.

```python
rp.compute_u = rp.compute_v = False
rp.n_threads = 16
# perform reduction
dcmp.reduce(rp)

# now we can acess V, R and U
# indices are sorted_ids of simplices == indices in fil.cells()
V = dcmp.v_data
print(f"Example of a V column: {V[-1]}, this chain contains cells:")

simplices = fil.simplices()
for sigma_idx in V[-1]:
    print(simplices[sigma_idx])
```

Now we can ask for a diagram. The `diagram` methods
uses the critical values from the filtration that was used to construct it to get
the values of simplices and returns diagrams in all dimensions. By default,
diagrams include points at infinity. If we only want the finite part,
we can specify that by `include_inf_points`.
```python
dgms = dcmp.diagram(include_inf_points=False)
```
To get diagram in one specific dimension, we can subscript
the object or call the `in_dimension` method.
Diagram will be returned as a NumPy array of shape `(n, 2)`

```python
dim=2
dgm_2 = dcmp.diagram().in_dimension(dim)
# or
dgm_2 = dcmp.diagram()[2]

assert type(dgm_2) is np.ndarray
```
Now, e.g. the birth coordinates are simply `dgm_2[:, 0]`.

If we want to know the peristence pairing, that is, which 
birth and death simplex gave us this particular point,
we can use `index_diagram`.
```python
dim=2
dgm_2 = dcmp.index_diagram().in_dimension(dim)
```
It is also a NymPy array (of integral type).
If needed, we can get all paired simplices, including those
with zero-persistence:
```
dgm_2 = dcmp.index_diagram(include_zero_persistence_points=True, include_inf_points=True).in_dimension(dim)
```

How to map this back to filtration? Let us take a look
at a single point in the index diagram:
```python
sigma_sorted_idx, tau_sorted_idx = dgm_2[0, :]
```
`sigma_sorted_idx` is the index of the birth simplex (triangle) in filtration order.
`tau_sorted_idx` is the index of the death simplex (tetrahedron) in filtration order.
There are many ways to get the original simplex:
* `sigma = fil.get_simplex(sigma_sorted_idx)` will return a simplex itself. So, `fil.get_simplex`
takes the `sorted_id` of a simplex and just accesses the vector of simplices at this index,
so it is cheap.
* `sigma_idx = fil.get_id_by_sorted_id(sigma_sorted_idx)` will return the `id` of `sigma`.
Recall that, by default, it is the index of `sigma` in the original list of simplices that was used to create the filtration.
This is convenient, if you have a parallel array of some information, one entry per simplex,
which you want to access.


## Topology Optimization

Topology optimization is performed by the `TopologyOptimizer` class.

```python
# fil is some filtration
import torch

simplex_values = torch.Tensor
```
Optimization is done in terms of _matching loss_: for a subset
of points in PD we set the desired location.
The object that encodes is called `Target`. You can create it manually,
but `TopologyOptimizer` provides you some functions for most common use cases.
Let us consider simplification: given some `epsilon`, we want to send
all points with persistence less than `epsilon` to the diagonal.

```python
#!/usr/bin/env python3

import numpy as np
import torch

import oineus as oin

# sample points from the unit circle
np.random.seed(1)

num_points = 50
noise_std_dev = 0.1

angles = np.random.uniform(low=0, high=2*np.pi, size=num_points)
x = np.cos(angles)
y = np.sin(angles)

x += np.random.normal(loc=0, scale=noise_std_dev, size=num_points)
y += np.random.normal(loc=0, scale=noise_std_dev, size=num_points)

pts = np.vstack((x, y)).T

# start with topological part

fil, longest_edges = oin.get_vr_filtration_and_critical_edges(pts, max_dim=2, max_radius=2.0, n_threads=1)

top_opt = oin.TopologyOptimizer(fil)

dim = 1
n = 2

eps = top_opt.get_nth_persistence(dim, n)
indices, values = top_opt.simplify(eps, oin.DenoiseStrategy.BirthBirth, dim)
critical_sets = top_opt.singletons(indices, values)
crit_indices, crit_values = top_opt.combine_loss(critical_sets, oin.ConflictStrategy.Max)

crit_indices = np.array(crit_indices, dtype=np.int32)
crit_edges = longest_edges[crit_indices, :]
crit_edges_x, crit_edges_y = crit_edges[:, 0], crit_edges[:, 1]

# torch part
# convert everything we need to torch.Tensor
pts = torch.Tensor(pts)
pts.requires_grad_(True)

crit_values = torch.Tensor(crit_values)
# verify the shapes: here we compute the lengths of critical edges
ic(torch.sum((pts[crit_edges_x, :] - pts[crit_edges_y, :])**2, axis=1).shape, crit_values.shape)
top_loss = torch.mean(torch.sum((pts[crit_edges_x, :] - pts[crit_edges_y, :])**2, axis=1) ** 0.5 - crit_values)

# let Torch figure the gradient on the coordinates
top_loss.backward()
```


