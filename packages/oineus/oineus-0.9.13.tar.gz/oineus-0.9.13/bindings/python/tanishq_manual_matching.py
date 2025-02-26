from icecream import ic
import time
import matplotlib.pyplot as plt
import oineus as oin
import numpy as np
import torch
import jax
import jax.numpy as jnp
import jax.random as jrandom
from jax import vmap,jit
import equinox as eqx
from ripser import ripser
from persim import plot_diagrams
WASS_DIST_Q = 2
DIM = 1
LATENT = 2
REG_PARAM = 1.0
STEPS = 0


#Plotting
def plot_critical_set(pts,step, edges, longest_edges, lengths , crit_values, mask_by_index,ax=plt,diagram=None):
    '''
    Parameters
    ----------
    pts : original data
    fil : filtration
    indices : indices of critical set

    Returns
    -------
    ax : plot
    '''

    if len(edges) == 0:
        return

    #Set up gradients
    l = lengths.detach().numpy()
    val = crit_values.numpy()
    edge_grads = {} 
    grad_values = []
    for key in mask_by_index:
        mask = mask_by_index[key]
        #value = len(l[mask] - val[mask])
        # value = np.sum(np.sign(l[mask]-val[mask]))
        value = np.sum(2*(l[mask] - val[mask]))
        edge_grads[key] = value
        grad_values.append(value)
    max_value = float(np.max(np.abs(grad_values)))
    #Normalize grads
    for key in edge_grads:
        edge_grads[key] = edge_grads[key]/max_value

    #Plotting
    fig = plt.figure(figsize=(15,5))
    fig.suptitle(f'Strategy={directory}, Loss={LOSS_TYPE}, Step={LEARNING_RATE}', fontsize=16)
    dig_axes = fig.add_subplot(1,2,2)
    plot_diagrams([diagram.in_dimension(0),diagram.in_dimension(1)],ax=dig_axes)
   
    pts_axes = fig.add_subplot(1,2,1)
    pts_axes.scatter(pts[:,0],pts[:,1],color='green')
    
    for key in edge_grads:
        edge_color = cm.viridis(edge_grads[key])
        edge = longest_edges[key]
        pts_axes.plot(pts[edge,0],pts[edge,1],c=edge_color,)

    #create colorbar 
    sm = cm.ScalarMappable(cmap=cm.viridis)
    sm.set_array(grad_values)
    # cbar = ax[0].colorbar(sm)
    #plt.plot(pts[:,0][edges.T],pts[:,1][edges.T],color='purple')

    #save figure
    plt.subplots_adjust(hspace=0.5, top=0.9, bottom=0.1)
    
    fig.savefig(f"Crit_sets/{str((step//100)%10) + str((step//10)%10) + str(step % 10) }.jpg")
    pts_axes.set_xlim(left=-1.4,right=1.2)
    fig.clf()
    plt.close(fig)
    return 
    
def plot_gradients(X,grad,step):
    grad = -LEARNING_RATE*grad
    plt.quiver(X[:,0],X[:,1], grad[:,0], grad[:,1],scale_units='xy',scale=0.01)
    plt.savefig(f'Gradients/Grad_at_{step}_{time.time()}.jpg')
    plt.clf()
    return

def diagram_plot(diagram,show=True):
    plt.clf()
    diagram_np = [diagram.in_dimension(0),diagram.in_dimension(1)]
    plot_diagrams(diagram_np)
    if show:
        plt.show()
    
def diag_grad(diagram,index_diagram,indices,values):
    #Draw arrows on the persistence diagram indicating the gradient direction of a point on the diagram
    indices_to_values = { indices[i]: values[i] for i in range(len(indices))}
    for (i,pair) in enumerate(index_diagram):
        point = diagram[i]
        # ic(point)
        birth_simplex, death_simplex = pair
        try:
            new_point = np.asarray([indices_to_values[birth_simplex],indices_to_values[death_simplex]])
        except:
            new_point = point
        grad = new_point - point
        plt.scatter(point[0],point[1],color='blue') 
        plt.plot([point[0],new_point[0]],[point[1],new_point[1]],color='black')
        plt.scatter(new_point[0],new_point[1],color='red')

def out_grid(model):
    Z = np.linspace(0,10.0,num=40)
    B = np.meshgrid(Z,Z)
    XX,YY = B[0].flatten(), B[1].flatten()
    grid = np.vstack([XX,YY]).T
    output = [ vec.detach().numpy() for vec in list(map(model.decode,torch.Tensor(grid).detach()))]
    return np.asarray(output) 
def save_outputs(outputs):
    plt.clf()
    for (step,output) in enumerate(outputs):
        out = output.detach().numpy()
        plt.scatter(out[:,0],out[:,1])
        plt.savefig(f'outputs/{str((step//100)%10) + str((step//10)%10) + str(step % 10) }.jpg')
        plt.clf()
    
def save_latent(latent_coords):
    global STEPS
    step = STEPS
    plt.clf()
    plt.scatter(latent_coords[:,0],latent_coords[:,1])
    plt.savefig(f"outputs/{str((step//100)%10) + str((step//10)%10) + str(step % 10) }.jpg")
    plt.clf()
    
#Topology Utils
def create_mask_by_index(og_crit_indices):
    crit_values_by_index = {}  
    for (i,index) in enumerate(og_crit_indices):
        if index not in crit_values_by_index:
            crit_values_by_index[index]  = []
        crit_values_by_index[index].append(i)
    return crit_values_by_index


#Model
class AutoEnc(torch.nn.Module):
    def __init__(self, in_size):
        super().__init__()
        self.encode = torch.nn.Sequential(torch.nn.Linear(in_size,LATENT),
                        torch.nn.ReLU(),
                        torch.nn.Linear(LATENT,LATENT)
                     )

        self.decode = torch.nn.Sequential(torch.nn.Linear(LATENT,in_size), 
                        torch.nn.ReLU(),
                        torch.nn.Linear(in_size,in_size)
                      )
    # def encode(self,x):
        # for layer in self.enc_layers:
            # x = layer(x)
        # return x
    # def decode(self,z):
        # for layer in self.dec_layers:
            # z = layer(z)
        # return z
    def __call__(self,x):
        #Returns the reconstruction of x
        x = self.encode(x)
        x = self.decode(x)
        return x
        

#Evalutation
def topological_loss(pts, space_diagram, model):
    global STEPS
    latent_coords = model.encode(pts)
    save_latent(latent_coords.detach().numpy())
    temp_latent_coords = np.asarray(latent_coords.detach().numpy(),dtype=np.double) 
    fil,longest_edges = oin.get_vr_filtration_and_critical_edges(temp_latent_coords, max_dim=2, max_radius=np.inf, n_threads=4)
    top_opt = oin.TopologyOptimizer(fil)
    latent_diagram = top_opt.compute_diagram(include_inf_points=False)
    latent_index_diagram = top_opt.compute_index_diagram(include_inf_points=False,include_zero_persistence_points=False)

    ic(latent_index_diagram[DIM])
    maximum_scale = np.max(latent_diagram[DIM])
    space_diagram = maximum_scale*space_diagram
    diag_list = []
    
    for i in range(space_diagram.shape[0]):
        birth =space_diagram[i][0]
        death =space_diagram[i][1]
        diag_list.append(oin.DiagramPoint_double(birth,death))

    indices, values = top_opt.match(diag_list, DIM, WASS_DIST_Q )

    #
    plt.clf()
    plt.scatter(space_diagram[:,0],space_diagram[:,1],color='orange')
    diag_grad(latent_diagram[DIM],latent_index_diagram[DIM],indices,values)
    plt.savefig(f"diags/{str((STEPS//100)%10) + str((STEPS//10)%10) + str(STEPS % 10) }.jpg")
    plt.clf()
    #
    
    critical_sets = top_opt.singletons(indices,values)
    crit_indices, crit_values = top_opt.combine_loss(critical_sets, oin.ConflictStrategy.Max)

    #Sorted index values
    og_crit_indices = np.array(crit_indices, dtype=np.int32)  
    mask_by_index = create_mask_by_index(og_crit_indices)
    crit_edges = longest_edges[og_crit_indices, :]
    crit_edges_s, crit_edges_t = crit_edges[:, 0], crit_edges[:, 1]
    crit_values = torch.Tensor(crit_values)
    lengths = torch.sum((latent_coords[crit_edges_s, :] - latent_coords[crit_edges_t, :])**2, axis=1) ** 0.5
    #plot_critical_set(X,0, crit_edges, longest_edges, lengths, crit_values, mask_by_index, diagram=dgm)
    #top_loss = torch.mean(torch.abs(lengths - crit_values))
    top_loss = torch.mean((lengths - crit_values)**2)
    STEPS = STEPS + 1
    return top_loss

def manual_topological_loss(pts, space_diagram, model):
    global STEPS
    latent_coords = model.encode(pts)
    save_latent(latent_coords.detach().numpy())
    temp_latent_coords = np.asarray(latent_coords.detach().numpy(),dtype=np.double) 
    fil,longest_edges = oin.get_vr_filtration_and_critical_edges(temp_latent_coords, max_dim=2, max_radius=np.inf, n_threads=4)
    top_opt = oin.TopologyOptimizer(fil)
    latent_diagram = top_opt.compute_diagram(include_inf_points=False)
    latent_index_diagram = top_opt.compute_index_diagram(include_inf_points=False,include_zero_persistence_points=False)

    maximum_scale = np.max(latent_diagram[DIM])
    space_diagram = maximum_scale*space_diagram
    lifetimes = np.asarray([death-birth for (birth,death) in space_diagram])
    feature_point = space_diagram[np.argmax(lifetimes)]

    latent_diagram_in_DIM = latent_diagram[DIM]
    latent_lifetimes = np.asarray([death-birth for (birth,death) in latent_diagram_in_DIM])
    most_pers_pair = latent_index_diagram[DIM][np.argmax(latent_lifetimes)] 
    indices, values = most_pers_pair, feature_point
    #
    plt.clf()
    plt.scatter(space_diagram[:,0],space_diagram[:,1],color='orange')
    diag_grad(latent_diagram[DIM],latent_index_diagram[DIM],indices,values)
    plt.savefig(f"diags/{str((STEPS//100)%10) + str((STEPS//10)%10) + str(STEPS % 10) }.jpg")
    plt.clf()
    #
    
    critical_sets = top_opt.singletons(indices,values)
    crit_indices, crit_values = top_opt.combine_loss(critical_sets, oin.ConflictStrategy.Max)

    #Sorted index values
    og_crit_indices = np.array(crit_indices, dtype=np.int32)  
    mask_by_index = create_mask_by_index(og_crit_indices)
    crit_edges = longest_edges[og_crit_indices, :]
    crit_edges_s, crit_edges_t = crit_edges[:, 0], crit_edges[:, 1]
    crit_values = torch.Tensor(crit_values)
    lengths = torch.sum((latent_coords[crit_edges_s, :] - latent_coords[crit_edges_t, :])**2, axis=1) ** 0.5
    #plot_critical_set(X,0, crit_edges, longest_edges, lengths, crit_values, mask_by_index, diagram=dgm)
    #top_loss = torch.mean(torch.abs(lengths - crit_values))
    top_loss = torch.mean((lengths - crit_values)**2)
    STEPS = STEPS + 1
    return top_loss



def reconstruction_loss(pts,reconstruction):
    MSE = torch.nn.MSELoss()
    return MSE(pts,reconstruction)
     
def regularizer(pts,model):
    return

#Training
def pre_train(pts,model):
    epochs = 100
    outputs = []
    losses = []
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr = 1e-1,
                                 weight_decay = 1e-8)
    for epoch in range(epochs):
        optimizer.zero_grad()
        reconstruction = model(pts)
        loss = reconstruction_loss(pts,reconstruction)
        loss.backward()
        optimizer.step()
        losses.append(loss.detach().numpy())
        outputs.append(reconstruction)
    return losses, outputs, model

def train(pts,model,losses,outputs):
    epochs = 30
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr = 1e-1,
                                 weight_decay = 1e-8)
    #computing diagram for points

    X = np.asarray(pts.detach().numpy(), dtype=np.double)
    fil = oin.get_vr_filtration(X,max_dim=2,max_radius=np.inf,n_threads=4)
    top_opt = oin.TopologyOptimizer(fil)
    og_diags = top_opt.compute_diagram(include_inf_points=False)
    # diagram_plot(og_diags,show=False)
    # plt.savefig("og_diagram.jpg")
    # plt.clf()
    
    og_diag = og_diags[DIM]
    og_maximum_scale = np.max(np.max(og_diag))
    og_diag = og_diag/og_maximum_scale
    plt.clf()
    plt.scatter(og_diag[:,0],og_diag[:,1],color='orange')
    plt.plot([0,1.5],[0,1.5],color='black')
    plt.xlim([0.0,1.5])
    plt.ylim([0.0,1.5])
    plt.savefig('og_diagram.jpg')
    plt.clf()
    global STEPS
    STEPS = 0
    for epoch in range(epochs):
        optimizer.zero_grad()
        reconstruction = model(pts)
        loss = reconstruction_loss(pts,reconstruction) + REG_PARAM*manual_topological_loss(pts,og_diag,model)
        loss.backward()
        optimizer.step()
        print(f"Grads applied {STEPS}")
        losses.append(loss.detach().numpy())
        outputs.append(reconstruction)
    return losses, outputs, model
 



if __name__=="__main__2":
    ic(STEPS)
    theta = np.random.random((100,))*2*np.pi
    Mat = np.random.random((2,3))
    pts = np.vstack([np.cos(theta),np.sin(theta)]).T
    pts = pts @ Mat
    pts = torch.Tensor(pts)
    max_dim = 2
    empty = oin.Diagrams_double(DIM+1)[DIM]
    aut = AutoEnc(pts.shape[1])
    losses, outputs, aut = pre_train(pts,aut)
    out = aut.encode(pts).detach().numpy()
    plt.scatter(out[:,0],out[:,1])
    plt.savefig(f"pretrained.jpg")
    plt.show()
    losses, outputs, aut = train(pts,aut,losses,outputs)
    plt.plot(losses)
    plt.show()

if __name__=="__main__":
    torch.manual_seed(45)
    np.random.seed(45)
    dat = np.loadtxt("example_data/annulus/dat.txt")[0:50]
    mat = np.random.random((2,3))
    pts = dat @ mat
    pts = torch.Tensor(pts)
    aut = AutoEnc(pts.shape[1])
    losses, outputs, aut = pre_train(pts,aut)
    out = aut.encode(pts).detach().numpy()
    plt.scatter(out[:,0],out[:,1])
    plt.savefig(f"pretrained.jpg")
    plt.clf()
    losses, outputs, aut = train(pts,aut,losses,outputs)
    plt.plot(losses)
    plt.show()
    
        
