import plotly.graph_objects as go
from neuron import h

def plot_neuron_morphology_plotly(neuron_model):
    data = []
    
    for sec in h.allsec():
        npts = sec.n3d()
        if npts == 0:
            continue
        
        x = [sec.x3d(i) for i in range(npts)]
        y = [sec.y3d(i) for i in range(npts)]
        z = [sec.z3d(i) for i in range(npts)]
        
        data.append(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='blue', width=4),
            name=sec.name()
        ))
        
    layout = go.Layout(
        title="Neuron Morphology",
        scene=dict(
            xaxis_title='X (µm)',
            yaxis_title='Y (µm)',
            zaxis_title='Z (µm)',
            aspectmode='data'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

