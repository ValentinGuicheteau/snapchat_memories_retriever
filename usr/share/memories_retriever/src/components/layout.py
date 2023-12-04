from dash import html, dcc
import dash_bootstrap_components as dbc

from src.components.file_input import file_input_panel
from src.components.folder import folder_tree_panel
from src.components.memory import picture, video
from src.components.map import memory_card


def layout():
    return html.Div([
        dcc.Location(id='url'),
        dcc.Loading(
            id="loading-1",
            type="default",
            className='loading-container',
            children=[
                
                dcc.Store(id='memories-store', storage_type='memory', data={}),
                dcc.Store(id='memory-id', storage_type='memory', data={'id': 0}),
                dcc.Store(id='current-memory', storage_type='memory', data={}),
                
                html.Button(id='import-btn-hidden', style={'display': 'none'}, n_clicks=0),

                dbc.Alert('', id='alert', color='success', is_open=False, duration=4000, style={'position': 'fixed', 'bottom': '1rem', 'right': '1rem'}),
                dbc.Alert('', id='alert-warning-add-folder', color='warning', is_open=False, duration=4000, style={'position': 'fixed', 'bottom': '1rem', 'right': '1rem'}),
                dbc.Alert('', id='alert-warning-folder-click', color='warning', is_open=False, duration=4000, style={'position': 'fixed', 'bottom': '1rem', 'right': '1rem'}),
                dbc.Alert('', id='alert-danger-import', color='danger', is_open=False, duration=4000, style={'position': 'fixed', 'bottom': '1rem', 'right': '1rem'}),
            ]
        ),

        
        html.H1(children='Sauvegarde de memories', style={'padding' : '1rem'}),

        html.Div(
            children=[
                html.Div(
                    children=[
                        file_input_panel(),
                        folder_tree_panel()
                    ],
                    id='left-content',
                ),
                iphone_layout(),

                html.Div(
                    children=[
                        html.H2('Date et localisation', id='memory-date-location'),
                        html.H3('', id='memory-date'),
                        memory_card(),

                    ],
                    id='right-content',
                )
                
            ], 
        className='row-content'),

        
    ], id='main-content')


def iphone_layout():
    return html.Div(
        children=[
        ],
        className='iphone-x', id='iphone-x')