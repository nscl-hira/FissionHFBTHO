#!/usr/bin/env python3
# Generate a namelist file for HFBTHO runs of Pb196
# Adam Anthony 6/4/2019

# Input: genPESFile.py Const1 Const2 ...
# Const1 is a lable of the lambdas to contrain
import sys

def usage():
    print("""\
Usage: genNamelist.py Const1 Const2 ...

    Const#: The list of lambdas to constrain (0, 1, 2, ...)
""")

if len(sys.argv) <= 1:
    usage()
    exit(1)


l = [0,0,0,0,0,0,0,0]
for arg in range(1,len(sys.argv),1):
    l[int(sys.argv[arg])-1] = 1

print("""
&HFBTHO_GENERAL
 number_of_shells = 31, oscillator_length = -1.0, basis_deformation = 0.2,
 proton_number = 82, neutron_number = 114, type_of_calculation = -1 /
&HFBTHO_INITIAL
 beta2_deformation = 0.1, beta3_deformation = 0.0, beta4_deformation = 0.0 /
&HFBTHO_ITERATIONS
 number_iterations = 500, accuracy = 1.E-5, restart_file = 2 /
&HFBTHO_FUNCTIONAL
 functional = 'UNE1', add_initial_pairing = F, type_of_coulomb = 2 /
&HFBTHO_PAIRING
 user_pairing = F, vpair_n = -250.0, vpair_p = -250.0,
 pairing_cutoff = 60.0, pairing_feature = 0.5 /
&HFBTHO_CONSTRAINTS
 lambda_values = 1, 2, 3, 4, 5, 6, 7, 8,
 lambda_active = %d, %d, %d, %d, %d, %d, %d, %d,
 expectation_values = 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 /
&HFBTHO_BLOCKING
 proton_blocking = 0, 0, 0, 0, 0, neutron_blocking = 0, 0, 0, 0, 0 /
&HFBTHO_PROJECTION
 switch_to_THO = 0, projection_is_on = 0,
 gauge_points = 1, delta_Z = 0, delta_N = 0 /
&HFBTHO_TEMPERATURE
 set_temperature = F, temperature = 0.0 /
&HFBTHO_FEATURES
 collective_inertia = T, fission_fragments = T, pairing_regularization = F,
 automatic_basis = F, localization_functions = T /
&HFBTHO_TDDFT
 filter = F, fragment_properties = F, real_Z = 49.7, real_N = 71.2  /
&HFBTHO_NECK
 set_neck_constrain = F, neck_value = 13.00  /
&HFBTHO_DEBUG
 number_Gauss = 40, number_Laguerre = 40, number_Legendre = 80,
 compatibility_HFODD = F, number_states = 1140, force_parity = F,
 print_time = 0 /

""" %(l[0],l[1],l[2],l[3],\
      l[4],l[5],l[6],l[7]))
