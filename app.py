import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from neuron import h
import random
from neuron_models import create_neuron_model, create_synapse, create_netstim, create_iclamp, create_vclamp
from simulation_engine import SimulationEngine, BatchSimulationEngine, analyze_spikes
from plotly_visualization import plot_neuron_morphology_plotly, plot_batch_results
import matplotlib.pyplot as plt
from matplotlib_visualization import plot_neuron_morphology_matplotlib, plot_batch_results_matplotlib, plot_membrane_potential_matplotlib, plot_raster_matplotlib
def clear_session_state():
    st.session_state.neuron_objects = {'synapses': [],'netcons': [],'netstims': [],'iclamps': [],'vclamps': [],'clamps': []}
    st.session_state.neuron_models = []
    st.session_state.engine = None
    st.session_state.data = {}
    st.session_state.batch_results = None
    st.session_state.simulation_running = False
    st.session_state.sweep_running = False
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'data' not in st.session_state:
    st.session_state.data = {}
if 'presets' not in st.session_state:
    st.session_state.presets = {}
if 'results_to_compare' not in st.session_state:
    st.session_state.results_to_compare = []
if 'neuron_models' not in st.session_state:
    st.session_state.neuron_models = []
if 'neuron_objects' not in st.session_state:
    st.session_state.neuron_objects = {'synapses': [],'netcons': [],'netstims': [],'iclamps': [],'vclamps': [],'clamps': []}
if 'selected_stimulus' not in st.session_state:
    st.session_state.selected_stimulus = 'IClamp'
if 'model_choice' not in st.session_state:
    st.session_state.model_choice = 'Simple Soma'
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None
st.set_page_config(layout="wide")
st.title('NEURON Network Simulator')
with st.expander("About this Simulator"):
    st.markdown("""
### NEURON Simulator Guide

#### Neuron Models

* **Simple Soma**: A basic model of a neuron consisting of a single section, representing the cell body. It's a fundamental model for studying basic neuron behavior.

* **Dendrite (Passive)**: A slightly more complex model with a cell body and a simple dendrite. The dendrite is "passive," meaning it doesn't have active voltage channels, so it just passively conducts electrical signals.

* **Multi-Compartment**: A more realistic model that includes a soma (cell body), multiple dendrites, and an axon. This model can capture more complex electrical properties and signal propagation.

#### Stimulus Types

* **IClamp (Current Clamp)**: Injects a fixed amount of electrical current into a neuron for a specific duration, which can be used to cause the neuron to fire an action potential.

* **VClamp (Voltage Clamp)**: Holds a neuron's membrane potential at a fixed voltage level. This is useful for studying the currents that flow through ion channels at different voltages.

* **NetStim (Network Stimulus)**: Generates a train of simulated action potentials that can be used to stimulate a synapse on a neuron. This represents input from another neuron in a network.

#### Synaptic Parameters

* **ExpSyn (Exponential Synapse)**: A simple synapse model where the postsynaptic current rises instantly and then decays exponentially over time. It's a basic model for a fast, excitatory synapse.

* **Exp2Syn (Double Exponential Synapse)**: A more realistic model where the postsynaptic current rises and decays with two different exponential time constants. This better approximates the time course of real synaptic currents.

#### Parameter Sweep

A **parameter sweep** systematically runs the same simulation multiple times while changing a specific parameter, like stimulus amplitude or synapse weight. The results are then analyzed to see how the parameter affects the network's average firing rate.

#### Plot Explanations

* **Neuron Morphology**: A 3D view of the physical shape of the neuron network. This shows how the cell bodies and dendrites are connected.

* **Membrane Potential**: A graph showing how the electrical voltage inside a neuron changes over time, often featuring rapid spikes known as action potentials.

* **Spike Raster Plot**: A visualization of the firing times of all neurons in the network. Each dot represents a spike from a single neuron at a specific time.

* **Batch Simulation Results**: A graph that summarizes the results of the parameter sweep. It shows how the network's average firing rate changes as a function of the parameter that was varied.
""")
col1, col2 = st.columns([1, 2])
def get_firing_rate(spikes, duration):
    if not spikes or duration == 0:
        return 0
    return len(spikes) / (duration / 1000)
with col1:
    st.header('Network and Model Parameters')
    st.subheader('Network Configuration')
    num_neurons = st.number_input('Number of Neurons', 1, 100, 5)
    connectivity_pattern = st.selectbox('Connectivity Pattern', ['All-to-All', 'Random'])
    if connectivity_pattern == 'Random':
        connection_prob = st.slider('Connection Probability', 0.0, 1.0, 0.2, 0.05)
    st.subheader('Neuron Model')
    st.session_state.model_choice = st.selectbox('Select Neuron Model Type (for all neurons)', ['Simple Soma', 'Dendrite (Passive)', 'Multi-Compartment'])
    rm = st.slider('Membrane Resistance (kOhm-cm²)', 100, 50000, 10000)
    cm = st.slider('Membrane Capacitance (uF/cm²)', 0.1, 5.0, 1.0)
    st.subheader('Stimulation')
    st.session_state.selected_stimulus = st.selectbox('Select Stimulus Type', ['IClamp', 'NetStim', 'VClamp'])
    target_neuron = st.number_input('Target Neuron Index for Stimulus', 0, num_neurons - 1, 0)
    if st.session_state.selected_stimulus == 'NetStim':
        st.subheader('Synaptic Parameters (for stimulus)')
        synapse_choice = st.selectbox('Select Synapse Type', ['ExpSyn', 'Exp2Syn'])
        syn_weight = st.slider('Stimulus Synaptic Weight', 0.001, 1.0, 0.05, 0.001)
    elif st.session_state.selected_stimulus == 'IClamp':
        st.subheader('Current Clamp Parameters')
        stim_delay = st.number_input('Stimulus Delay (ms)', 0, 5000, 100)
        stim_dur = st.number_input('Stimulus Duration (ms)', 1, 5000, 100)
        stim_amp = st.number_input('Stimulus Amplitude (nA)', -20.0, 20.0, 2.0, 0.1)
    elif st.session_state.selected_stimulus == 'VClamp':
        st.subheader('Voltage Clamp Parameters')
        vc_dur = st.number_input('Clamp Duration (ms)', 1, 5000, 100)
        vc_level = st.number_input('Clamp Level (mV)', -100.0, 50.0, -20.0, 0.1)
    st.subheader('Simulation Control')
    duration = st.number_input('Simulation Duration (ms)', 100, 5000, 500)
    dt = st.number_input('Timestep (ms)', 0.001, 1.0, 0.025)
    if st.button('Start Simulation', key='start_sim_button'):
        st.session_state.simulation_running = True
        clear_session_state()
        h.load_file('stdrun.hoc')
        for i in range(num_neurons):
            model_dict = create_neuron_model(st.session_state.model_choice, rm, cm)
            st.session_state.neuron_models.append(model_dict)
        inter_neuron_syn_weight = 0.02
        for i, pre_neuron_dict in enumerate(st.session_state.neuron_models):
            for j, post_neuron_dict in enumerate(st.session_state.neuron_models):
                if i == j: continue
                connect = False
                if connectivity_pattern == 'All-to-All':
                    connect = True
                elif connectivity_pattern == 'Random' and random.random() < connection_prob:
                    connect = True
                if connect:
                    syn = create_synapse(post_neuron_dict['soma'], 'ExpSyn')
                    st.session_state.neuron_objects['synapses'].append(syn)
                    source_sec = pre_neuron_dict['soma']
                    if 'axon' in pre_neuron_dict and pre_neuron_dict['axon'] is not None:
                        apc = h.APCount(pre_neuron_dict['axon'](1))
                        netcon = h.NetCon(apc, syn)
                        st.session_state.neuron_objects['netcons'].append(netcon)
                        netcon.weight[0] = inter_neuron_syn_weight
                        netcon.delay = 5
                    else:
                        netcon = h.NetCon(pre_neuron_dict['soma'](1)._ref_v, syn, sec=pre_neuron_dict['soma'])
                        st.session_state.neuron_objects['netcons'].append(netcon)
                        netcon.weight[0] = inter_neuron_syn_weight
                        netcon.delay = 5
        target_model_dict = st.session_state.neuron_models[target_neuron]
        if st.session_state.selected_stimulus == 'NetStim':
            syn = create_synapse(target_model_dict['soma'], synapse_choice)
            st.session_state.neuron_objects['synapses'].append(syn)
            netstim = create_netstim(h)
            st.session_state.neuron_objects['netstims'].append(netstim)
            netcon = h.NetCon(netstim, syn)
            st.session_state.neuron_objects['netcons'].append(netcon)
            netcon.weight[0] = syn_weight
        elif st.session_state.selected_stimulus == 'IClamp':
            iclamp = create_iclamp(target_model_dict['soma'], stim_delay, stim_dur, stim_amp)
            st.session_state.neuron_objects['iclamps'].append(iclamp)
        elif st.session_state.selected_stimulus == 'VClamp':
            vclamp = create_vclamp(target_model_dict['soma'], vc_dur, vc_level)
            st.session_state.neuron_objects['vclamps'].append(vclamp)
        st.session_state.engine = SimulationEngine(st.session_state.neuron_models, duration, dt)
        st.session_state.data = st.session_state.engine.run_simulation()
        st.session_state.simulation_running = False
        st.success('Simulation complete!')
    st.subheader('Parameter Sweep & Batch Analysis')
    sweep_param = st.selectbox('Parameter to Sweep', ['stim_amp', 'syn_weight'])
    trials_per_set = st.number_input('Trials per parameter set', 1, 10, 1)
    sweep_values = []
    if sweep_param == 'stim_amp':
        min_val = st.number_input('Min Amplitude (nA)', -10.0, 10.0, 0.1, 0.1)
        max_val = st.number_input('Max Amplitude (nA)', -10.0, 10.0, 2.0, 0.1)
        step_val = st.number_input('Step (nA)', 0.1, 5.0, 0.5, 0.1)
        sweep_values = np.arange(min_val, max_val + step_val, step_val)
    elif sweep_param == 'syn_weight':
        min_val = st.number_input('Min Weight', 0.0, 1.0, 0.01, 0.01)
        max_val = st.number_input('Max Weight', 0.0, 1.0, 0.2, 0.01)
        step_val = st.number_input('Step', 0.01, 0.5, 0.05, 0.01)
        sweep_values = np.arange(min_val, max_val + step_val, step_val)
    if st.button('Run Parameter Sweep'):
        st.session_state.sweep_running = True
        progress_bar = st.progress(0)
        batch_engine = BatchSimulationEngine()
        st.session_state.batch_results = batch_engine.run_sweep(sweep_param, sweep_values, trials_per_set, progress_bar, num_neurons, st.session_state.model_choice, rm, cm, duration, dt, connectivity_pattern, connection_prob if connectivity_pattern == 'Random' else None)
        st.session_state.sweep_running = False
        st.success('Batch simulation complete!')
with col2:
    st.header('Simulation Results')
    visualization_library = st.selectbox("Select Plotting Library", ["Plotly", "Matplotlib"])
    if st.session_state.neuron_models:
        st.subheader('Neuron Morphology')
        if visualization_library == "Plotly":
            fig_morph = plot_neuron_morphology_plotly(st.session_state.neuron_models)
            st.plotly_chart(fig_morph)
        else:
            fig_morph = plot_neuron_morphology_matplotlib(st.session_state.neuron_models)
            st.pyplot(fig_morph)
    if st.session_state.simulation_running:
        st.info("Simulation in progress...")
    if st.session_state.data:
        st.subheader('Membrane Potential')
        if visualization_library == "Plotly":
            fig_v = go.Figure()
            num_neurons_in_data = len(st.session_state.neuron_models)
            for i in range(num_neurons_in_data):
                fig_v.add_trace(go.Scatter(x=st.session_state.data['time'], y=st.session_state.data[f'neuron_{i}_v_soma'], mode='lines', name=f'Neuron {i}'))
            fig_v.update_layout(title='Membrane Potential Traces', xaxis_title='Time (ms)', yaxis_title='Membrane Potential (mV)')
            st.plotly_chart(fig_v)
        else:
            fig_v = plot_membrane_potential_matplotlib(st.session_state.data, len(st.session_state.neuron_models))
            st.pyplot(fig_v)
        st.subheader('Spike Raster Plot')
        spike_threshold = st.slider('Spike Detection Threshold (mV)', -50.0, 0.0, -20.0, 1.0)
        if visualization_library == "Plotly":
            fig_raster = go.Figure()
            all_spike_times = []
            all_neuron_indices = []
            spike_counts = []
            num_neurons_in_data = len(st.session_state.neuron_models)
            for i in range(num_neurons_in_data):
                voltages = st.session_state.data[f'neuron_{i}_v_soma']
                times = st.session_state.data['time']
                spikes = analyze_spikes(voltages, times, spike_threshold)
                all_spike_times.extend(spikes)
                all_neuron_indices.extend([i] * len(spikes))
                spike_counts.append((i, len(spikes)))
            if all_spike_times:
                fig_raster.add_trace(go.Scatter(x=all_spike_times, y=all_neuron_indices, mode='markers', marker=dict(symbol='circle', size=4, color='cyan', line=dict(width=1, color='darkblue')), name='Spikes'))
                fig_raster.update_layout(title='Spike Raster Plot', xaxis_title='Time (ms)', yaxis_title='Neuron Index', yaxis=dict(tickmode='linear', dtick=1), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                fig_raster.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                fig_raster.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                st.plotly_chart(fig_raster)
            else:
                st.warning("No spikes detected. Try increasing stimulus strength or adjusting parameters.")
        else:
            all_spike_times = []
            all_neuron_indices = []
            spike_counts = []
            num_neurons_in_data = len(st.session_state.neuron_models)
            for i in range(num_neurons_in_data):
                voltages = st.session_state.data[f'neuron_{i}_v_soma']
                times = st.session_state.data['time']
                spikes = analyze_spikes(voltages, times, spike_threshold)
                all_spike_times.extend(spikes)
                all_neuron_indices.extend([i] * len(spikes))
                spike_counts.append((i, len(spikes)))
            fig_raster = plot_raster_matplotlib(all_spike_times, all_neuron_indices)
            st.pyplot(fig_raster)
        st.subheader('Spike Detection Results')
        spike_text = "\n".join([f"Neuron {i}: {count} spikes" for i, count in spike_counts])
        st.text_area("Spike counts per neuron:", value=spike_text, height=150, key="spike_counts", disabled=True)
    if st.session_state.batch_results is not None:
        st.subheader('Batch Simulation Results')
        if visualization_library == "Plotly":
            fig_batch = plot_batch_results(st.session_state.batch_results)
            st.plotly_chart(fig_batch)
        else:
            fig_batch = plot_batch_results_matplotlib(st.session_state.batch_results)
            st.pyplot(fig_batch)

