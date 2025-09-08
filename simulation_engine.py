from neuron import h

class SimulationEngine:
    def __init__(self, model, duration, dt):
        self.model = model
        self.duration = duration
        self.dt = dt
        
        self.v_soma_vec = h.Vector()
        self.v_dend_vec = h.Vector()
        self.t_vec = h.Vector()
        
        self.v_soma_vec.record(self.model(0.5)._ref_v)
        
        # Check if the model has a dendrite section
        for sec in h.allsec():
            if sec.name() == 'dend1':
                self.v_dend_vec.record(sec(0.5)._ref_v)
                break
        
        self.t_vec.record(h._ref_t)
        
    def run_simulation(self):
        h.dt = self.dt
        h.t = 0
        h.finitialize(-65)
        
        h.continuerun(self.duration)
        
        data = {'time': list(self.t_vec), 'v_soma': list(self.v_soma_vec)}
        if len(self.v_dend_vec) > 0:
            data['v_dend'] = list(self.v_dend_vec)
        
        return data

    def pause_simulation(self):
        pass

    def reset_simulation(self):
        h.finitialize(-65)

