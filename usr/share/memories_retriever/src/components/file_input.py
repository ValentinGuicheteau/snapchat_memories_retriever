from dash import html, dcc
import dash_bootstrap_components as dbc


def file_input_panel():
    return dbc.Card([
        dbc.CardHeader('Import de l\'export des mémories'),
        dbc.CardBody([
            html.Label('Veuillez sélectionner un export des mémories snapchat'),
            dcc.Upload(
                id='memories-file-upload',
                children=html.Div([
                    '',
                    html.A('Sélectionner un fichier')
                ]),
                
            ),
            # radio button to select the type of file
            html.Label('Veuillez sélectionner le type de fichier'),
            dcc.RadioItems(
                id='file-type',
                options=[
                    {'label': 'JSON', 'value': 'json'},
                    {'label': 'HTML', 'value': 'html', 'disabled': True}
                ],
                value='json'
            ),
            
            #  number input to select the number of memories to import
            html.Label('Débuter l\'import à partir du memory n°'),
            dbc.Input(
                id='start-from',
                type='number',
                value=0,
                min=0
            ),
            # button to start the import

            dbc.Button('Importer', id='import-btn', color='primary', className='mt-2', disabled=True)

        ])

    ], id='file-input-panel',
        className='left-panels'
)
