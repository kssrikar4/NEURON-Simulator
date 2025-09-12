import plotly.graph_objects as go
import plotly.express as px
from neuron import h
def plot_neuron_morphology_plotly(neuron_models):
    data = []
    colors = px.colors.qualitative.Plotly
    for i, neuron_model in enumerate(neuron_models):
        color = colors[i % len(colors)]
        for sec in h.allsec():
            if h.distance(neuron_model(0.5), sec(0.5)) < 1000:
                npts = sec.n3d()
                if npts == 0:
                    sec.pt3dclear()
                    sec.pt3dadd(0, 0, 0, sec.diam)
                    sec.pt3dadd(sec.L, 0, 0, sec.diam)
                    npts = 2
                x = [sec.x3d(j) for j in range(npts)]
                y = [sec.y3d(j) for j in range(npts)]
                z = [sec.z3d(j) for j in range(npts)]
                data.append(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color=color, width=4),
                    name=f'Neuron {i} - {sec.name()}'
                ))
    layout = go.Layout(
        title="Neuron Morphology",
        scene=dict(
            xaxis_title='X (µm)',
            yaxis_title='Y (µm)',
            zaxis_title='Z (µm)',
            aspectmode='data'
        ),
        showlegend=True
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

