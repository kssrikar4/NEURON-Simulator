import random
from neuron import h
from neuron_models import create_neuron_model, create_synapse, create_iclamp, create_netstim
def analyze_spikes(voltage_vec, time_vec, threshold):
    spikes = []
    refractory_period = 2.0
    last_spike_time = -refractory_period
    for j in range(1, len(voltage_vec)):
        if (voltage_vec[j] > threshold and voltage_vec[j - 1] <= threshold and (time_vec[j] - last_spike_time) > refractory_period):
            spikes.append(time_vec[j])
            last_spike_time = time_vec[j]
    return spikes
class SimulationEngine:
    def __init__(self, models, duration, dt):
        self.models = models
        self.duration = duration
        self.dt = dt
        self.v_soma_vecs = []
        self.t_vec = h.Vector()
        for model in self.models:
            v_vec = h.Vector()
            v_vec.record(model['soma'](0.5)._ref_v)
            self.v_soma_vecs.append(v_vec)
        self.t_vec.record(h._ref_t)
    def run_simulation(self):
        h.dt = self.dt
        h.t = 0
        h.finitialize(-65)
        h.continuerun(self.duration)
        data = {'time': list(self.t_vec)}
        for i, v_vec in enumerate(self.v_soma_vecs):
            data[f'neuron_{i}_v_soma'] = list(v_vec)
        return data
    def pause_simulation(self):
        pass
    def reset_simulation(self):
        h.finitialize(-65)
class BatchSimulationEngine:
    def run_sweep(self, param_to_sweep, sweep_values, trials_per_set, progress_bar, num_neurons, model_choice, rm, cm, duration, dt, connectivity_pattern, connection_prob):
        results = {'param_name': [param_to_sweep] * len(sweep_values), 'param_value': [], 'avg_firing_rate': []}
        total_steps = len(sweep_values) * trials_per_set
        completed_steps = 0
        for value in sweep_values:
            all_firing_rates = []
            for _ in range(trials_per_set):
                h.finitialize(-65)
                neuron_models = []
                for i in range(num_neurons):
                    model_dict = create_neuron_model(model_choice, rm, cm)
                    neuron_models.append(model_dict)
                for i, pre_neuron_dict in enumerate(neuron_models):
                    for j, post_neuron_dict in enumerate(neuron_models):
                        if i == j: continue
                        connect = False
                        if connectivity_pattern == 'All-to-All':
                            connect = True
                        elif connectivity_pattern == 'Random' and random.random() < connection_prob:
                            connect = True
                        if connect:
                            syn = create_synapse(post_neuron_dict['soma'], 'ExpSyn')
                            if 'axon' in pre_neuron_dict and pre_neuron_dict['axon'] is not None:
                                apc = h.APCount(pre_neuron_dict['axon'](1))
                                netcon = h.NetCon(apc, syn)
                                netcon.weight[0] = 0.02
                            else:
                                netcon = h.NetCon(pre_neuron_dict['soma'](1)._ref_v, syn, sec=pre_neuron_dict['soma'])
                                netcon.weight[0] = 0.02
                if param_to_sweep == 'stim_amp':
                    iclamp = create_iclamp(neuron_models[0]['soma'], 100, 100, value)
                elif param_to_sweep == 'syn_weight':
                    syn = create_synapse(neuron_models[0]['soma'], 'ExpSyn')
                    netstim = create_netstim(h)
                    netcon = h.NetCon(netstim, syn)
                    netcon.weight[0] = value
                engine = SimulationEngine(neuron_models, duration, dt)
                data = engine.run_simulation()
                total_spikes = 0
                for i in range(num_neurons):
                    voltages = data[f'neuron_{i}_v_soma']
                    times = data['time']
                    spikes = analyze_spikes(voltages, times, -20)
                    total_spikes += len(spikes)
                avg_firing_rate = (total_spikes / num_neurons) / (duration / 1000) if num_neurons > 0 else 0
                all_firing_rates.append(avg_firing_rate)
                completed_steps += 1
                progress_bar.progress(completed_steps / total_steps)
            results['param_value'].append(value)
            results['avg_firing_rate'].append(sum(all_firing_rates) / trials_per_set)
        return results

