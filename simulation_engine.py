from neuron import h
class SimulationEngine:
    def __init__(self, models, duration, dt):
        self.models = models
        self.duration = duration
        self.dt = dt
        self.v_soma_vecs = []
        self.t_vec = h.Vector()
        for model in self.models:
            v_vec = h.Vector()
            v_vec.record(model(0.5)._ref_v)
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

