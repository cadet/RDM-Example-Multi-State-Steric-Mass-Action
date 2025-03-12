# ---
# jupyter:
#   jupytext:
#     formats: md:myst,ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# (lwe_example_concentration)=
# # Concentration Gradients
#
# ```
# {figure} ./figures/flow_sheet_concentration.svg
# Flow sheet for load-wash-elute process using a single inlet.
# ```

# %% [markdown]
# Tentacle Resin used for IEX (cation -CEX))= Fractogel EMD SO^-_3 -> selectivity, unusual behavior with high load
# 4 different load experiments -> "shoulder (peak) under overloaded conditions"
# therapeutic mAb from CHO culture on Fractogel (SO_3)^-
# Load, Wash, Gradient Elution (linear salt gradient)
#

# %%
# %%time
import numpy as np

from CADETProcess.processModel import ComponentSystem
from CADETProcess.processModel import MultistateStericMassAction
from CADETProcess.processModel import Inlet, GeneralRateModel, Outlet
from CADETProcess.processModel import FlowSheet
from CADETProcess.processModel import Process

# Component System
component_system = ComponentSystem()
component_system.add_component('Salt')
component_system.add_component('A')

# Binding Model
#parameters: bound_states, adsorption_rate, desorption_rate, characteristic_charge, 
#steric_factor, conversion_rate, capacity, reference_liquid_phase_conc, reference_solid_phase_conc, name, is_kinetic, n_binding_sites, _bound_states
binding_model = MultistateStericMassAction(component_system, bound_states=[1,2], name='MultistateSMA')
binding_model.is_kinetic = True
binding_model.adsorption_rate = [0.0, 1.1e31, 7.7e26 ] #adsorption rate 1= 1.1e31, state2 = 7.7e26
binding_model.desorption_rate = [0.0, 5.9e31, 2.0e36] #desorption rate1 = 5.9e31, state2 = 2e36
binding_model.characteristic_charge = [0.0, 9.6, 24.7] #für alle components und ihre verschiedenen, state1 = 9.6, state2 = 24.7
binding_model.steric_factor = [0.0, 47.8, 65.9] #state1 = 47.8, state2 = 65.9
binding_model.conversion_rate = [1.0, 1.0, 9.4e39, 9.5, 1.0] #MSSMA_RATES = [1.0, rate_{0,0}, rate_{0,1}, rate_{1,0}, rate_{1,1}] = [comp0fromBnd0toBnd0,comp1fromBnd0toBnd0, comp1fromBnd0toBnd1, comp1fromBnd1toBnd0, comp1fromBnd1toBnd1]
binding_model.capacity = 223.55 #ionic capacity = 223.55mM = 223.55 mol/m^3
binding_model.reference_liquid_phase_conc = 520.0 #= maximal salt conc. during elution = cref  = 520mM 
binding_model.reference_solid_phase_conc = 223.55 #column capacity = qref 


# Unit Operations
inlet = Inlet(component_system, name='inlet')
inlet.flow_rate = 4.0333e-8  #2.42 mL/min -> 4.03e−8 m³/s 

#Transport Model for mobile phase in the column 
column = GeneralRateModel(component_system, name='column')
column.binding_model = binding_model
column.length = 0.215 #0.215m (Table A1)
column.diameter = 0.012 #"1.2cm high column (3.1)"column geometry known from Äkta log book and manufacturing data (3.2)
column.bed_porosity = 0.34  #εc = V(interstitial)/(V(interstitial)+V(beads)) = bulk porosity
column.particle_radius = 3.25e-5 #rp
column.particle_porosity = 0.39 #εp = V(channels)/(V(channels)+ V(solid)
column.axial_dispersion = 10.0e-7 #bulk liquid, Dax
column.film_diffusion = column.n_comp*[2.0e-5] #porous beads, kf
column.pore_diffusion = [0.0, 9.0e-12] #porous beads, Dp = 9e-12
column.surface_diffusion = column.n_bound_states*[0.0] #nicht gegeben
#column.convection bulk liquid ?
#interstitial velocity u = 0.0011438 m/s

#concentrations: cref = 520mM , qref = 223.55mM  (unbound/bound?)

column.c = [520.0e-6, 0] #initial conc. of reactor, erster wert in array automatisch konstante in mol/m^3
#column.cp  default = column.c
column.q = [binding_model.capacity, 0.0, 0.0] #initial conc. of bound phase

outlet = Outlet(component_system, name='outlet')

# Flow Sheet
flow_sheet = FlowSheet(component_system)

flow_sheet.add_unit(inlet)
flow_sheet.add_unit(column)
flow_sheet.add_unit(outlet, product_outlet=True)

flow_sheet.add_connection(inlet, column)
flow_sheet.add_connection(column, outlet)


# %% [markdown]
# ```{figure} ./figures/events_concentration.svg
# Events of load-wash-elute process using a single inlet and modifying its concentration.
# ```

# %%
# Process Load of mAb feed: 118.2g/L = 0.106mM 
 # loadings of: [g/L] 72.5, 82.8, 93.1, 118.2 with differing lwe times
process = Process(flow_sheet, 'lwe')
process.cycle_time = 200 * 60.0 #200min

load_duration = 74.15 * 60
wash_duration = 27.7*60
t_gradient_start = load_duration + wash_duration
gradient_duration = 88.1*60
salt_gradient = (500.0-69.97)/88.1

c_load = np.array([69.97, 0.106])  
c_wash = np.array([69.97, 0.0])
#c_elute = np.array([69.97, 0.0, salt_gradient])  # 15 CV(column volumes) salt gradient from 69.97 mM NaCl buffer to 500mM NaCl
c_elute =  np.array([500.0, 0.0])
gradient_slope = (c_elute - c_wash)/gradient_duration
c_gradient_poly = np.array(list(zip(c_wash, gradient_slope)))  #

process.add_event('load', 'flow_sheet.inlet.c', c_load)
process.add_event('wash', 'flow_sheet.inlet.c',  c_wash, load_duration)
#process.add_event('elute','flow_sheet.inlet.c', c_elute, load_duration + wash_duration, indices =[(0,0), (0,1)])
process.add_event('grad_start', 'flow_sheet.inlet.c', c_gradient_poly, t_gradient_start)
process.plot_events()

# %%

# %%
#c_load = np.array([69.97, 1.0])  
#c_wash = np.array([69.97, 0.0])
#c_elute = np.array([69.97, 0.0, salt_gradient])  # 15 CV(column volumes) salt gradient from 69.97 mM NaCl buffer to 500mM NaCl
#gradient_slope = np.array([1234])
#c_gradient_poly = np.array(list(zip(c_load, gradient_slope)))
#print(c_gradient_poly)

# %%
print(__name__)
if __name__ == '__main__':
    print("HI")
    from CADETProcess.simulator import Cadet
    process_simulator = Cadet()

    simulation_results = process_simulator.simulate(process)

    from CADETProcess.plotting import SecondaryAxis
    sec = SecondaryAxis()
    sec.components = ['Salt']
    sec.y_label = '$c_{salt}$'

    simulation_results.solution.column.outlet.plot(secondary_axis=sec)

# %%
column.parameters

# %%
