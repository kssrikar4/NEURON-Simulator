import plotly.graph_objects as go
import plotly.express as px
from neuron import h
def plot_neuron_morphology_plotly(neuron_models):
    data = []
    colors = px.colors.qualitative.Plotly
    for i, model_dict in enumerate(neuron_models):
        color = colors[i % len(colors)]
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
            zaxis_title='Z (µm)'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig
def plot_batch_results(batch_results):
    fig = go.Figure(data=go.Scatter(
        x=batch_results['param_value'],
        y=batch_results['avg_firing_rate'],
        mode='lines+markers',
        marker=dict(symbol='circle', size=8),
        line=dict(width=2),
        name='Avg Firing Rate'
    ))
    fig.update_layout(
        title=f"Network Firing Rate vs. {batch_results['param_name'][0]}",
        xaxis_title=batch_results['param_name'][0],
        yaxis_title="Average Firing Rate (Hz)",
        hovermode="x unified",
        template="plotly_white"
    )
    return fig

