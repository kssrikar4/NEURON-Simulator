import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from neuron import h
import random
from neuron_models import create_neuron_model, create_synapse, create_netstim, create_iclamp, create_vclamp
from simulation_engine import SimulationEngine
from plotly_visualization import plot_neuron_morphology_plotly
def clear_session_state():
    st.session_state.neuron_objects = {
        'synapses': [],
        'netcons': [],
        'netstims': [],
        'iclamps': [],
        'vclamps': []
    }
    st.session_state.neuron_models = []
    st.session_state.engine = None
    st.session_state.data = {}
    st.session_state.simulation_running = False
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
    st.session_state.neuron_objects = {}
if 'selected_stimulus' not in st.session_state:
    st.session_state.selected_stimulus = 'IClamp'
if 'model_choice' not in st.session_state:
    st.session_state.model_choice = 'Simple Soma'
st.set_page_config(layout="wide")
st.title('NEURON Network Simulator')
col1, col2 = st.columns([1, 2])
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
    if st.button('Start Simulation'):
        st.session_state.simulation_running = True
        clear_session_state()
        h.load_file('stdrun.hoc')
        for i in range(num_neurons):
            model = create_neuron_model(st.session_state.model_choice, rm, cm)
            st.session_state.neuron_models.append(model)
        inter_neuron_syn_weight = 0.02 
        for i, pre_neuron in enumerate(st.session_state.neuron_models):
            for j, post_neuron in enumerate(st.session_state.neuron_models):
                if i == j: continue
                connect = False
                if connectivity_pattern == 'All-to-All':
                    connect = True
                elif connectivity_pattern == 'Random' and random.random() < connection_prob:
                    connect = True
                if connect:
                    syn = h.ExpSyn(post_neuron(0.5))
                    st.session_state.neuron_objects['synapses'].append(syn)
                    source_sec = pre_neuron
                    if 'axon' in [s.name() for s in h.allsec() if h.distance(pre_neuron(0.5), s(0.5)) > 0]:
                         for sec in h.allsec():
                            if sec.name() == 'axon' and h.distance(pre_neuron(0.5), sec(0.5)) < 200:
                                source_sec = sec
                                break
                    netcon = h.NetCon(source_sec(1)._ref_v, syn, sec=source_sec)
                    netcon.weight[0] = inter_neuron_syn_weight
                    netcon.delay = 5
                    st.session_state.neuron_objects['netcons'].append(netcon)
        target_model = st.session_state.neuron_models[target_neuron]
        if st.session_state.selected_stimulus == 'NetStim':
            syn = create_synapse(target_model, synapse_choice)
            st.session_state.neuron_objects['synapses'].append(syn)
            netstim = create_netstim(h)
            st.session_state.neuron_objects['netstims'].append(netstim)
            netcon = h.NetCon(netstim, syn)
            st.session_state.neuron_objects['netcons'].append(netcon)
            netcon.weight[0] = syn_weight
        elif st.session_state.selected_stimulus == 'IClamp':
            iclamp = create_iclamp(target_model, stim_delay, stim_dur, stim_amp)
            st.session_state.neuron_objects['iclamps'].append(iclamp)
        elif st.session_state.selected_stimulus == 'VClamp':
            vclamp = create_vclamp(target_model, vc_dur, vc_level)
            st.session_state.neuron_objects['vclamps'].append(vclamp)
        st.session_state.engine = SimulationEngine(st.session_state.neuron_models, duration, dt)
        st.session_state.data = st.session_state.engine.run_simulation()
        st.session_state.simulation_running = False
        st.success('Simulation complete!')
    if st.button('Reset Simulation'):
        clear_session_state()
        st.experimental_rerun()
with col2:
    st.header('Simulation Results')
    if st.session_state.neuron_models:
        st.subheader('Neuron Morphology')
        fig_morph = plot_neuron_morphology_plotly(st.session_state.neuron_models)
        st.plotly_chart(fig_morph)
    if st.session_state.simulation_running:
        st.info("Simulation in progress...")
    if st.session_state.data:
        st.subheader('Membrane Potential')
        fig_v = go.Figure()
        num_neurons_in_data = sum(1 for key in st.session_state.data if 'v_soma' in key)
        for i in range(num_neurons_in_data):
            fig_v.add_trace(go.Scatter(
                x=st.session_state.data['time'], 
                y=st.session_state.data[f'neuron_{i}_v_soma'], 
                mode='lines', 
                name=f'Neuron {i}'
            ))
        fig_v.update_layout(title='Membrane Potential Traces', xaxis_title='Time (ms)', yaxis_title='Membrane Potential (mV)')
        st.plotly_chart(fig_v)
        st.subheader('Spike Raster Plot')
        spike_threshold = st.slider('Spike Detection Threshold (mV)', -50.0, 0.0, -20.0, 1.0)
        fig_raster = go.Figure()
        all_spike_times = []
        all_neuron_indices = []
        spike_counts = []
        for i in range(num_neurons_in_data):
            voltages = st.session_state.data[f'neuron_{i}_v_soma']
            times = st.session_state.data['time']
            spikes = []
            refractory_period = 2.0
            last_spike_time = -refractory_period
            for j in range(1, len(voltages)):
                if (voltages[j] > spike_threshold and 
                    voltages[j-1] <= spike_threshold and 
                    (times[j] - last_spike_time) > refractory_period):
                    spikes.append(times[j])
                    last_spike_time = times[j]
            all_spike_times.extend(spikes)
            all_neuron_indices.extend([i] * len(spikes))
            spike_counts.append((i, len(spikes)))
        if all_spike_times:
            fig_raster.add_trace(go.Scatter(
                x=all_spike_times, 
                y=all_neuron_indices, 
                mode='markers', 
                marker=dict(
                    symbol='circle',
                    size=4, 
                    color='cyan',  
                    line=dict(width=1, color='darkblue')
                ),
                name='Spikes'
            ))
            fig_raster.update_layout(
                title='Spike Raster Plot', 
                xaxis_title='Time (ms)', 
                yaxis_title='Neuron Index',
                yaxis=dict(tickmode='linear', dtick=1),
                plot_bgcolor='rgba(0,0,0,0)',  
                paper_bgcolor='rgba(0,0,0,0)'  
            )
            fig_raster.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig_raster.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            st.plotly_chart(fig_raster)
        else:
            st.warning("No spikes detected. Try increasing stimulus strength or adjusting parameters.")
        st.subheader('Spike Detection Results')
        spike_text = "\n".join([f"Neuron {i}: {count} spikes" for i, count in spike_counts])
        st.text_area(
            "Spike counts per neuron:", 
            value=spike_text, 
            height=150, 
            key="spike_counts",
            disabled=True  
        )
