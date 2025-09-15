import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from neuron import h
def plot_neuron_morphology_matplotlib(neuron_models):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = plt.cm.get_cmap('tab10', len(neuron_models))
    for i, model_dict in enumerate(neuron_models):
        color = colors(i)
        sections_to_plot = [model_dict['soma']] + model_dict['dendrites']
        if model_dict['axon']:
            sections_to_plot.append(model_dict['axon'])
        for sec in sections_to_plot:
            npts = sec.n3d()
            if npts == 0:
                sec.pt3dclear()
                sec.pt3dadd(0, 0, 0, sec.diam)
                sec.pt3dadd(sec.L, 0, 0, sec.diam)
                npts = 2
            x = [sec.x3d(j) for j in range(npts)]
            y = [sec.y3d(j) for j in range(npts)]
            z = [sec.z3d(j) for j in range(npts)]
            ax.plot(x, y, z, color=color, linewidth=2, label=f'Neuron {i} - {sec.name()}')
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_zlabel('Z (µm)')
    ax.set_title("Neuron Morphology")
    return fig
def plot_membrane_potential_matplotlib(data, num_neurons):
    fig, ax = plt.subplots()
    for i in range(num_neurons):
        ax.plot(data['time'], data[f'neuron_{i}_v_soma'], label=f'Neuron {i}')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Membrane Potential (mV)')
    ax.set_title('Membrane Potential Traces')
    ax.legend()
    ax.grid(True)
    return fig
def plot_raster_matplotlib(all_spike_times, all_neuron_indices):
    fig, ax = plt.subplots()
    ax.plot(all_spike_times, all_neuron_indices, '|', color='black')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Neuron Index')
    ax.set_title('Spike Raster Plot')
    ax.set_yticks(range(max(all_neuron_indices) + 1))
    ax.grid(True, axis='y')
    return fig
def plot_batch_results_matplotlib(batch_results):
    fig, ax = plt.subplots()
    ax.plot(batch_results['param_value'], batch_results['avg_firing_rate'], marker='o', linestyle='-')
    ax.set_xlabel(batch_results['param_name'][0])
    ax.set_ylabel('Average Firing Rate (Hz)')
    ax.set_title(f"Network Firing Rate vs. {batch_results['param_name'][0]}")
    ax.grid(True)
    return fig

