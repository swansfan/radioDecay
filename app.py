import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
import decay

colourUndecayed = '#bf1f2e'
colourDecayed = '#3c6bba'
colourPlotBackground = '#f9fbfb'
colourMarker = '#476ab4'
colourLineExpDecay = '#97d4ae'
maxX = 25
maxY = 40
atom_x = np.tile(np.arange(0.5, float(maxX + 0.5), 1.), int(maxX))
atom_y = np.repeat(np.arange(0.5, float(maxY + 0.5), 1.), int(maxY))
decayConstant = 1. / 10.  # probability of decay per time interval - equivalent to a decay constant
maxTimeSteps = 20
# initialise an array for defining the marker colours for decayed/undecayed atoms for each timestep
marker_colour = np.empty((maxX * maxY, maxTimeSteps + 1), dtype=np.dtype('U7'))

# Run random decay
atoms, atomsdecayed, atomsremaining = decay.simdecay(maxX, maxY, maxTimeSteps, decayConstant)
print('original',atomsremaining)

external_stylesheets = [dbc.themes.FLATLY, 'assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)
server = app.server
app.title='Modelling RadioactiveDecay'

body = html.Div([
    dbc.Row([
        dbc.Col(
            html.H1("Radioactive Decay")
            , width=4),
        dbc.Col(
            html.Div(
                [html.H3(id='IDoutputText'), html.P('Years Elapsed')],
                id="IDoutput",
                className="mini_container")
            , width=2),
        dbc.Col(
            html.Div(
                [html.H3(id='IDtotalText'), html.P('Total Atoms')],
                id="IDnumAtoms",
                className="mini_container")
            , width=2),
        dbc.Col(
            html.Div(
                [html.H3(id='IDremainText'), html.P('Number Remaining')],
                id="IDnumRemaining",
                className="mini_container")
            , width=2),
        dbc.Col(
            html.Div(
                [html.H3(id='IDdecayedText'), html.P('Number Decayed')],
                id="IDnumDecayed",
                className="mini_container")
            , width=2),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='IDatomsPlot',
                          config={'displayModeBar': False},
                          figure={'data': [go.Scatter(
                              x=atom_x,
                              y=atom_y,
                              mode='markers',
                              name='Undecayed Atom',
                              marker={'size': 12, 'color': colourUndecayed}
                          )],
                              'layout': go.Layout(
                                  #title='Atoms',
                                  xaxis={'ticks': '', 'showticklabels': False,
                                         'showgrid': False,
                                         'range': [0, 20],
                                         'zeroline': False},
                                  yaxis={'ticks': '', 'showticklabels': False,
                                         'range': [0, 1000],
                                         'showgrid': False,
                                         'zeroline': False},
                                  plot_bgcolor=colourPlotBackground,
                                  paper_bgcolor=colourPlotBackground,
                                  hovermode=False,
                                  shapes=[{'type': 'circle', 'x0': 0.5, 'y0': 0.5, 'x1': 0.8, 'y1': 0.8,
                                          'xref': 'paper', 'yref': 'paper'}],
                                  margin={'t': 10, 'r': 10, 'b': 10, 'l': 10}
                              )}
                          )
                , className='pretty_container')
            , width=4),
        dbc.Col(
            html.Div(
                dcc.Graph(id='IDdecayTimeseriesPlot',
                          figure={'data': [go.Scatter(
                              x=[],
                              y=[],
                              name='Exponential Decay',
                              mode='lines',
                              marker={'size': 15}
                          )],
                              'layout': go.Layout(
                                  xaxis={'title': 'Time (years)'},
                                  yaxis={'title': 'Number of Original Atoms Remaining'},
                                  margin={'t': 60, 'r': 60, 'b': 60, 'l': 60},
                                  plot_bgcolor=colourPlotBackground,
                                  paper_bgcolor=colourPlotBackground,
                                  hovermode='closest'
                              )}
                          )
                , className='pretty_container')
            , width=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.P(
                'Click or drag the slider to change the time:',
                className='control_label'
            ),
            html.Div(id='IDsliderLabel')]
            , width=2),
        dbc.Col(
            html.Div(
                dcc.Slider(id='IDstepSlider',
                           min=0,
                           max=maxTimeSteps,
                           step=1,
                           value=0,
                           updatemode='drag',
                           marks={i: 't={}y'.format(i) for i in range(maxTimeSteps + 1)},
                           ),
                className='mini_container')
            , width=8),
    ])
])

app.layout = html.Div([body])


@app.callback(Output(component_id='IDoutputText', component_property='children'),
              [Input(component_id='IDstepSlider', component_property='value')])
def update_div(value):
    return value


@app.callback([Output(component_id='IDdecayTimeseriesPlot', component_property='figure'),
               Output(component_id='IDtotalText', component_property='children'),
               Output(component_id='IDremainText', component_property='children'),
               Output(component_id='IDdecayedText', component_property='children')],
              [Input(component_id='IDstepSlider', component_property='value')])
def update_timeseriesgraph(currentstep):
    traces = []
    # First add in the trace for the analytical solution to the exponential decay equation
    xdata, ydata = decay.calcdecay(maxX, maxY, maxTimeSteps, decayConstant)
    updatefigure = (go.Scatter(
        x=xdata,
        y=ydata,
        name='Exponential Decay',
        mode='lines',
        line={'dash':'dash'},
        opacity=1.0,
        marker={'size': 15, 'color': colourLineExpDecay}
    ))
    traces.append(updatefigure)
    # Now add in the trace for the simulated random decay plot
    # xdata = np.arange(len(atomsremaining)).reshape(len(atomsremaining), 1)
    xdata = np.arange(0, currentstep + 1, 1)
    ydata = atomsremaining[range(0, len(atomsremaining))]
    print('in slider ydata',ydata)
    print('in slider atomsremaining',atomsremaining)
    numatoms = atomsremaining[0]
    numremaining = atomsremaining[currentstep]
    numdecayed = numatoms - numremaining
    updatefigure = (go.Scatter(
        x=xdata,
        y=ydata,
        name='Random (Simulated) Decay',
        mode='markers',
        opacity=1.0,
        marker={'size': 8, 'color': colourMarker, 'symbol': 'x'}
    ))
    traces.append(updatefigure)
    updatelayout = (go.Layout(
        xaxis={'title': 'Time (years)',
               'mirror': True,
               'range': [0, 20.5]},
        yaxis={'title': 'Number of Original Atoms Remaining',
               'mirror': True,
               'range': [0, 1090]},
        legend={'x': 0.74, 'y': 1.00,
                'borderwidth': 1.0,
                'bordercolor': '#efeded'},
        margin={'t': 60, 'r': 60, 'b': 60, 'l': 60},
        plot_bgcolor=colourPlotBackground,
        paper_bgcolor=colourPlotBackground,
        hovermode='closest'))
    return {
               'data': traces,
               'layout': updatelayout
           }, numatoms, numremaining, numdecayed
#'Total Atoms: {}'.format(numatoms), \
#'Remaining Atoms: {}'.format(numremaining), \
#'Decayed Atoms: {}'.format(numdecayed)


#           atomsremaining[len(atomsremaining)], 'Remaining Atoms', \
#           1000 - atomsremaining[len(atomsremaining)], 'Decayed Atoms'


@app.callback(Output(component_id='IDatomsPlot', component_property='figure'),
              [Input(component_id='IDstepSlider', component_property='value')])
def update_atom_box(currentstep):
    traces = []
    xdata = atom_x
    ydata = atom_y
    atoms_state = np.reshape(atoms[:, :, currentstep], (np.size(atoms[:, :, currentstep])))
    marker_colour[:, currentstep] = np.where(atoms_state == 0, colourDecayed, colourUndecayed)
    updatefigure = (go.Scatter(
        x=xdata,
        y=ydata,
        mode='markers',
        marker=dict(size=12, color=(marker_colour[:, currentstep]))
    ))
    # print(xdata, ydata)
    updatelayout = (go.Layout(
        #title='Atoms',
        xaxis={'ticks': '', 'showticklabels': False,
               'showgrid': False,
               'zeroline': False},
        yaxis={'ticks': '', 'showticklabels': False,
               'showgrid': False,
               'zeroline': False},
        legend={'x': 0.74, 'y': 0.50,
                'borderwidth': 1.0,
                'bordercolor': '#efeded'},
        plot_bgcolor=colourPlotBackground,
        paper_bgcolor=colourPlotBackground,
        hovermode=False,
        # Shapes for manual key
        shapes=[{'type': 'circle', 'x0': 0.20, 'y0': -0.05, 'x1': 0.225, 'y1': -0.025,
                 'xref': 'paper', 'yref': 'paper', 'line_color': colourUndecayed,
                 'fillcolor': colourUndecayed},
                {'type': 'circle', 'x0': 0.60, 'y0': -0.05, 'x1': 0.625, 'y1': -0.025,
                 'xref': 'paper', 'yref': 'paper', 'line_color': colourDecayed,
                 'fillcolor': colourDecayed}],
        annotations=[{'text': '<b>Key:</b>', 'x': 0.10, 'y': -0.063, 'showarrow': False,
                 'xref': 'paper', 'yref': 'paper', 'font_size': 14},
                     {'text': 'Undecayed Atom', 'x': 0.24, 'y': -0.060, 'showarrow': False,
                      'xref': 'paper', 'yref': 'paper'},
                {'text': 'Decayed Atom', 'x': 0.82, 'y': -0.060, 'showarrow': False,
                 'xref': 'paper', 'yref': 'paper'}],
        margin={'t': 0, 'r': 15, 'b': 40, 'l': 10}
    ))
    traces.append(updatefigure)
    return {
        'data': traces,
        'layout': updatelayout
    }


if __name__ == '__main__':
    app.run_server()
