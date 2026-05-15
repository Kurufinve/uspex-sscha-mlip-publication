NPROC = 10

### SSCHA relaxation parameters

PRESSURE = 150 
TEMPERATURE = 300     
N_CONFIGS = [1000,3000]      # Number of configurations in each ensemble
MAX_ITERATIONS = 200  # Number of relaxation steps at which a new dymanical matrix is generated
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


# MLIP parameters
path_to_mlip = '/home/dpoletaev/soft/mlip-3/bin/mlp'
mlip_run_command = f'mpirun -np {NPROC} {path_to_mlip}'
pot_name  = 'pot.almtp'

pretrain_on_rand_structures = [True,False] # we do not pretrain on radnom structures because we using CHGNet for generation of initial dynamical matrix
train_on_initial_ensemble = False
train_on_every_ensemble = [True,True] # if True the MTP is trained every time the new ensemble is generated  
train_local_mtps = False # if True the new MTP is trained from scratch every time the training new set is generated (e.g. from ensemble)  
retrain = False # if we wish to retrain the MTP on structures produced with extrapolation control (better to make it False)
energy_weight = 1.0
force_weight = 1.0
stress_weight = 1.0
include_stress = True

standardize_structure = False
write_energy_file = [False,True] 

input_structure = 'POSCAR' # name of file with input structure 
#autoreplicate = [False,True,True] # if True, the number of replications in each direction calculated automativcally based on desired minimum number of atoms in the supercell Nfinal
nq1 = [1,2] # supercell multiplicity in the 1st direction
nq2 = [1,2] # supercell multiplicity in the 2nd direction
nq3 = [1,2] # supercell multiplicity in the 3rd direction
calculator = 'LAMMPS' # calculator for energies, forces, and stresses
specorder = ['La','H']

continue_from_dyn = [False,True]

# calculator parameters

calculator_files =  [pot_name] # file with interatomic potentials 

if retrain == True:
    threshold = 10
    threshold_break = 50
    iteration_limit = 500
    calculator_parameters = {'pair_style': f'mlip load_from={calculator_files[0]} extrapolation_control=true extrapolation_control:threshold_break={threshold_break} extrapolation_control:threshold={threshold} extrapolation_control:add_grade_feature=true extrapolation_control:save_extrapolative_to=preselected.cfg',
                            'pair_coeff': ['* *'],}
elif retrain == False:
    calculator_parameters = {'pair_style': f'mlip load_from={calculator_files[0]} extrapolation_control=false',
                            'pair_coeff': ['* *'],}

calculator_parameters_relax = {'fix': [f'ensemble all box/relax iso {PRESSURE*10000} \n dump relax all custom 1 relax.dump id type xsu ysu zsu fx fy fz vx vy vz'],
                               'minimize': '0.0 0.0001 10000 10000000'}

calculator_run_command = f'~/interface-lammps-mlip-3/lmp_mpi'

relax_zero_ab_initio = False # we do not relax structure at 0 K with DFT
relax_zero_iap = False # we do not relax structure at 0 K with MTP

init_dyn_iap = True # if True we calculate initial dynamical matrix with MTP 
init_dyn_ab_initio = False

relax_sscha_iap = True # if True we conduct SSCHA relaxation with MTP
relax_sscha_ab_initio = False # if True we conduct SSCHA relaxation with ab initio engine


correct_pressure = True
correct_free_energy = [False,True]

### Parameters for ab initio calculator that will be used if the additional training of MTP is necessary

ab_initio_calculator = "VASP" # we use quantum espresso calulator

np_ab_initio = 10

ab_initio_parameters = {
                        'PREC':  'Accurate',
                        'ENCUT':  520,
                        'EDIFF':  1e-5,
                        'ISMEAR':  1,
                        'SIGMA':  0.060,
                        'ISTART':  0,
                        'LCHARG':  'FALSE',
                        'LWAVE':  'FALSE', 
                        'LREAL': 'Auto'                       
                        }

ab_initio_pseudos = '~/potpaw_PBE'
 
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


