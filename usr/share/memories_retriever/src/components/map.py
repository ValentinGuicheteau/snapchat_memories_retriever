from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px


def memory_card(lat=0.0, lon=0.0):
    return dbc.Card(
        [
            dbc.CardHeader('Lieu du memory'),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id='map',
                        figure=memory_map(lat, lon)
                    )
                ]
            )
        ]
    )


def memory_map(lat, lon):
    return px.scatter_mapbox(lat=[lat], lon=[lon], zoom=12, height=300).update_layout(mapbox_style='open-street-map').update_layout(margin={"r":0,"t":0,"l":0,"b":0})