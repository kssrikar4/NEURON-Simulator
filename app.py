import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from neuron import h
from neuron_models import create_neuron_model, create_synapse, create_netstim, create_iclamp, create_vclamp
from simulation_engine import SimulationEngine
from plotly_visualization import plot_neuron_morphology_plotly

def reset_neuron_state():
    """Clears all NEURON objects and resets the state to prevent memory errors."""
    h.allsec()
    for sec in h.allsec():
        h.delete_section(sec=sec)
    h.pop_section()

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
if 'neuron_model_instance' not in st.session_state:
    st.session_state.neuron_model_instance = None
if 'selected_stimulus' not in st.session_state:
    st.session_state.selected_stimulus = 'NetStim'
if 'model_choice' not in st.session_state:
    st.session_state.model_choice = 'Simple Soma'

st.set_page_config(layout="wide")

st.title('NEURON Simulator Web App')

col1, col2 = st.columns([1, 2])

with col1:
    st.header('Model and Parameters')
    st.session_state.model_choice = st.selectbox('Select Neuron Model', ['Simple Soma', 'Dendrite (Passive)', 'Multi-Compartment'])
    
    st.subheader('Model Parameters')
    rm = st.slider('Membrane Resistance (kOhm-cm²)', 100, 50000, 10000)
    cm = st.slider('Membrane Capacitance (uF/cm²)', 0.1, 5.0, 1.0)

    st.subheader('Stimulation Type')
    st.session_state.selected_stimulus = st.selectbox('Select Stimulus Type', ['NetStim', 'IClamp', 'VClamp'])

    if st.session_state.selected_stimulus == 'NetStim':
        st.subheader('Synaptic Parameters')
        synapse_choice = st.selectbox('Select Synapse Type', ['ExpSyn', 'Exp2Syn', 'AlphaSynapse'])
        connectivity_choice = st.selectbox('Select Connectivity', ['All-to-All', 'Random'])
        syn_weight = st.slider('Synaptic Weight', 0.001, 1.0, 0.05, 0.001)

    elif st.session_state.selected_stimulus == 'IClamp':
        st.subheader('Current Clamp Parameters')
        stim_delay = st.number_input('Stimulus Delay (ms)', 0, 5000, 100)
        stim_dur = st.number_input('Stimulus Duration (ms)', 1, 5000, 100)
        stim_amp = st.number_input('Stimulus Amplitude (nA)', -2.0, 2.0, 0.5, 0.01)
    
    elif st.session_state.selected_stimulus == 'VClamp':
        st.subheader('Voltage Clamp Parameters')
        vc_dur = st.number_input('Clamp Duration (ms)', 1, 5000, 100)
        vc_level = st.number_input('Clamp Level (mV)', -100.0, 50.0, -20.0, 0.1)
    
    st.subheader('Simulation Control')
    duration = st.number_input('Simulation Duration (ms)', 100, 5000, 500)
    dt = st.number_input('Timestep (ms)', 0.001, 1.0, 0.025)
    
    if st.button('Start Simulation'):
        st.session_state.simulation_running = True
        reset_neuron_state()
        h.load_file('stdrun.hoc')
        neuron_model = create_neuron_model(st.session_state.model_choice, rm, cm)
        st.session_state.neuron_model_instance = neuron_model

        if st.session_state.selected_stimulus == 'NetStim':
            syn = create_synapse(neuron_model, synapse_choice)
            netstim = create_netstim(h)
            netcon = h.NetCon(netstim, syn, sec=neuron_model)
            netcon.weight[0] = syn_weight
        elif st.session_state.selected_stimulus == 'IClamp':
            iclamp = create_iclamp(neuron_model, stim_delay, stim_dur, stim_amp)
        elif st.session_state.selected_stimulus == 'VClamp':
            vclamp = create_vclamp(neuron_model, vc_dur, vc_level)
        
        st.session_state.engine = SimulationEngine(neuron_model, duration, dt)
        st.session_state.data = st.session_state.engine.run_simulation()
        st.session_state.simulation_running = False
        st.success('Simulation complete!')

    if st.button('Reset Simulation'):
        st.session_state.engine = None
        st.session_state.data = {}
        st.session_state.simulation_running = False
        reset_neuron_state()
        st.experimental_rerun()

    st.subheader('Export/Import')
    if st.button('Export Data to CSV'):
        df = pd.DataFrame(st.session_state.data)
        st.download_button(
            label="Download Data",
            data=df.to_csv().encode('utf-8'),
            file_name='neuron_data.csv',
            mime='text/csv',
        )

    st.subheader('Save/Load Configuration')
    config = {
        'model_choice': st.session_state.model_choice,
        'rm': rm,
        'cm': cm,
        'selected_stimulus': st.session_state.selected_stimulus,
        'duration': duration,
        'dt': dt,
    }
    if st.session_state.selected_stimulus == 'NetStim':
        config.update({'synapse_choice': synapse_choice, 'connectivity_choice': connectivity_choice, 'syn_weight': syn_weight})
    elif st.session_state.selected_stimulus == 'IClamp':
        config.update({'stim_delay': stim_delay, 'stim_dur': stim_dur, 'stim_amp': stim_amp})
    elif st.session_state.selected_stimulus == 'VClamp':
        config.update({'vc_dur': vc_dur, 'vc_level': vc_level})

    config_json = json.dumps(config)
    st.download_button(
        label="Save Configuration",
        data=config_json,
        file_name='neuron_config.json',
        mime='application/json',
    )
    
    uploaded_file = st.file_uploader("Load Configuration", type=['json'])
    if uploaded_file is not None:
        config_data = json.load(uploaded_file)
        st.session_state.presets = config_data
        st.info("Configuration loaded. Parameters will be updated on rerun.")

    st.subheader('Batch Simulation')
    batch_name = st.text_input('Batch Simulation Name')
    if st.button('Save Current Config as Preset'):
        st.session_state.presets[batch_name] = config
        st.success(f"Preset '{batch_name}' saved.")
    
    if st.button('Run Batch Simulation'):
        for name, preset in st.session_state.presets.items():
            reset_neuron_state()
            h.load_file('stdrun.hoc')
            neuron_model = create_neuron_model(preset['model_choice'], preset['rm'], preset['cm'])
            if preset['selected_stimulus'] == 'NetStim':
                syn = create_synapse(neuron_model, preset['synapse_choice'])
                netstim = create_netstim(h)
                netcon = h.NetCon(netstim, syn, sec=neuron_model)
                netcon.weight[0] = preset['syn_weight']
            elif preset['selected_stimulus'] == 'IClamp':
                iclamp = create_iclamp(neuron_model, preset['stim_delay'], preset['stim_dur'], preset['stim_amp'])
            engine = SimulationEngine(neuron_model, preset['duration'], preset['dt'])
            result = engine.run_simulation()
            st.session_state.results_to_compare.append({'name': name, 'data': result})
        st.success("Batch simulation complete!")

with col2:
    st.header('Simulation Results')
    
    if st.session_state.neuron_model_instance:
        st.subheader('Neuron Morphology')
        fig_morph = plot_neuron_morphology_plotly(st.session_state.neuron_model_instance)
        st.plotly_chart(fig_morph)

    if st.session_state.simulation_running:
        st.info("Simulation in progress...")
    
    if st.session_state.data:
        st.subheader('Membrane Potential')
        data_soma = go.Scatter(x=st.session_state.data['time'], y=st.session_state.data['v_soma'], mode='lines', name='Soma')
        fig_v = go.Figure(data=[data_soma])

        if 'v_dend' in st.session_state.data and st.session_state.model_choice == 'Multi-Compartment':
            data_dend = go.Scatter(x=st.session_state.data['time'], y=st.session_state.data['v_dend'], mode='lines', name='Dendrite')
            fig_v.add_trace(data_dend)

        fig_v.update_layout(title='Membrane Potential', xaxis_title='Time (ms)', yaxis_title='Membrane Potential (mV)')
        st.plotly_chart(fig_v)

        st.subheader('Spike Raster Plot')
        spikes = [t for i, t in enumerate(st.session_state.data['time']) if st.session_state.data['v_soma'][i] > -20]
        fig_raster = go.Figure(data=go.Scatter(
            x=spikes, y=[1] * len(spikes), mode='markers', name='Spikes'
        ))
        fig_raster.update_layout(title='Spike Raster Plot', xaxis_title='Time (ms)', yaxis_title='Neuron', yaxis=dict(showgrid=False, showticklabels=False))
        st.plotly_chart(fig_raster)

    if st.session_state.results_to_compare:
        st.subheader('Comparison of Runs')
        fig_compare = go.Figure()
        for result in st.session_state.results_to_compare:
            fig_compare.add_trace(go.Scatter(x=result['data']['time'], y=result['data']['v_soma'], mode='lines', name=result['name']))
        fig_compare.update_layout(title='Comparison of Runs', xaxis_title='Time (ms)', yaxis_title='Membrane Potential (mV)')
        st.plotly_chart(fig_compare)
    
    st.subheader('Simulation Logs')
    log_area = st.empty()
    log_area.text('No logs yet.')
    
    st.subheader('External Stimuli')
    stim_file = st.file_uploader('Upload Stimulus Dataset (CSV)', type=['csv'])
    if stim_file is not None:
        stim_data = pd.read_csv(stim_file)
        st.write('Uploaded Stimulus Data:')
        st.dataframe(stim_data)

