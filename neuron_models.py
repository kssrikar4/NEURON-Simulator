import random
from neuron import h

def create_neuron_model(model_name, rm, cm):
    try:
        h.nrn_load_dll("./channels.dll")
    except RuntimeError:
        print("channels.dll not found. Using default channels.")
    
    h.pop_section()

    if model_name == 'Simple Soma':
        soma = h.Section(name='soma')
        soma.L = 10
        soma.diam = 10
        soma.Ra = 100
        soma.insert('pas')
        soma.g_pas = 1 / rm
        soma.e_pas = -65
        soma.cm = cm
        h.define_shape()
        return soma
    
    elif model_name == 'Dendrite (Passive)':
        soma = h.Section(name='soma')
        dend = h.Section(name='dend')
        dend.connect(soma(1))
        
        for sec in [soma, dend]:
            sec.L = 100
            sec.diam = 2
            sec.Ra = 100
            sec.insert('pas')
            sec.g_pas = 1 / rm
            sec.e_pas = -65
            sec.cm = cm
        h.define_shape()
        return soma
        
    elif model_name == 'Multi-Compartment':
        soma = h.Section(name='soma')
        dend1 = h.Section(name='dend1')
        dend2 = h.Section(name='dend2')
        dend3 = h.Section(name='dend3')
        axon = h.Section(name='axon')
        
        dend1.connect(soma(1))
        dend2.connect(dend1(1))
        dend3.connect(dend2(1))
        axon.connect(soma(0))
        
        for sec in [soma, dend1, dend2, dend3, axon]:
            sec.L = 100
            sec.diam = 2
            sec.Ra = 100
            sec.insert('pas')
            sec.g_pas = 1 / rm
            sec.e_pas = -65
            sec.cm = cm
            
        soma.insert('hh')
        axon.insert('hh')
        h.define_shape()
        return soma
    
    return None

def create_synapse(neuron_model, syn_type):
    if syn_type == 'ExpSyn':
        syn = h.ExpSyn(neuron_model(0.5))
        syn.tau = 2
        syn.e = 0
    elif syn_type == 'Exp2Syn':
        syn = h.Exp2Syn(neuron_model(0.5))
        syn.tau1 = 0.5
        syn.tau2 = 2
        syn.e = 0
    elif syn_type == 'AlphaSynapse':
        syn = h.AlphaSynapse(neuron_model(0.5))
        syn.tau = 1
        syn.e = 0
    
    return syn

def create_netstim(h_obj):
    ns = h_obj.NetStim()
    ns.interval = 10
    ns.number = 1
    ns.start = 50
    return ns

def create_iclamp(neuron_model, delay, duration, amp):
    stim = h.IClamp(neuron_model(0.5))
    stim.delay = delay
    stim.dur = duration
    stim.amp = amp
    return stim

def create_vclamp(neuron_model, dur, level):
    vc = h.VClamp(neuron_model(0.5))
    vc.dur[0] = dur
    vc.amp[0] = level
