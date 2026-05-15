NPROC = 10

### SSCHA relaxation parameters

PRESSURE = 150 
TEMPERATURE = 300     
N_CONFIGS = [1000,3000]      # Number of configurations in each ensemble
MAX_ITERATIONS = 100  # Number of relaxation steps at which a new dymanical matrix is generated
RELAX_SIMPLE = True     # Perform the NVT relaxation keeping the unit cell volume unchanged
RELAX_NVT = True     # Perform the NVT relaxation allowing to relax lattice vectors keeping the unit cell volume unchanged
RELAX_NPT = True    # Perform the NPT relaxation allowing to relax the lattice vectors and volume to the desired pressure

### SSCHA minimization parameters

min_step_dyn = 0.05     # The minimization step on the dynamical matrix
min_step_struc = 0.05   # The minimization step on the structure
kong_liu_ratio = 0.5     # The parameter that estimates whether the ensemble is still good
gradi_op = "all" # Check the stopping condition on both gradients
meaningful_factor = 0.001 # How much small the gradient should be before I stop?
root_representation = 'normal' # can be 'normal', 'sqrt', or 'root4'
precond_dyn = True # should be false if 'sqrt' or 'root4' root_repesenattion is used
# root_representation = 'sqrt' # can be 'normal', 'sqrt', or 'root4'
# precond_dyn = False # should be false if 'sqrt' or 'root4' root_repesenattion is used

device = 'cuda' # or 'cpu'

iap_type = 'mattersim' # mattersim
pot_name  = '../mattersim-v1.0.0-5M.pth' # universal mattersim iap

standardize_structure = False
input_structure = 'POSCAR' # name of file with input structure
output_structure = 'CONTCAR'
write_energy_file = [False,True] 
 
nq1 = [1,2] # supercell multiplicity in the 1st direction
nq2 = [1,2] # supercell multiplicity in the 2nd direction
nq3 = [1,2] # supercell multiplicity in the 3rd direction
calculator = 'ase' # calculator for energies, forces, and stresses
specorder = ['La','H']

continue_from_dyn = [False,True]

relax_zero_iap = [True,False]  # if True we relax structure at 0 K with IAP

init_dyn_iap =  [True,False] # if True we calculate initial dynamical matrix with IAP 
init_dyn_ab_initio = False

relax_sscha_iap = [True,True] # if True we conduct SSCHA relaxation with IAP
relax_sscha_ab_initio = False # if True we conduct SSCHA relaxation with ab initio engine

correct_pressure = True
correct_free_energy = [False,True]

### Parameters for ab initio calculator that will be used if the additional training of IAP is necessary

ab_initio_calculator = "VASP" # we use quantum espresso calulator

np_ab_initio = 10

ab_initio_parameters = {
                        'PREC':  'Accurate',
                        'ENCUT':  500,
                        'EDIFF':  1e-5,
                        'ISMEAR':  1,
                        'SIGMA':  0.060,
                        'ISTART':  0,
                        'LCHARG':  'FALSE',
                        'LWAVE':  'FALSE', 
                        'LREAL': 'Auto',
                        }

ab_initio_pseudos = '../potpaw_PBE'
 
ab_initio_kresol = 0.05

ab_initio_run_command = f"mpirun -np {np_ab_initio} vasp_std"

use_hpc = False  # if True, an hpc for ab initio calculations will be used, if False the ab initio calculation will run on the same computer as the main script

min_distances = {'La La': 2.0, 'La H': 1.0, 'H H': 0.6} # min_distance constraints for generated structures 
## if generate_good_only = True, the algorithm will try to stiffen the current dynamical matrix 
## by multiplying its frequencies by stiffen_factor during the SSCHA relaxation
## in order to generate ensemble only with structures that satisfy min_distance constraints
try_generate_good_only = False 
min_good_fraction = 0.5 # minimal fraction of good structures in ensemble
stiffen_factor = 2
include_bad_structures = True # if True include structures that do not satisfy the min_distance constraints into SSCHA ensembles
