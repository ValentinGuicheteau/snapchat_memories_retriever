from dash import Dash, html, dcc, callback, Output, Input, State, no_update, ALL, MATCH, callback_context
import plotly.express as px
import pandas as pd

from src.components.layout import layout

import dash_bootstrap_components as dbc

import json
import base64
import requests
from urllib.parse import urlparse, unquote
import os

from src.components.memory import picture, video
from src.components.folder import create_folder_item, load_folders, giga_usage_to_string
from src.components.map import memory_map

# Crée une application Dash
app = Dash(__name__, external_stylesheets=['./static/css/app.css', './static/css/iphone.css', dbc.themes.SANDSTONE, dbc.icons.FONT_AWESOME])

# Initialise la mise en page de l'application
app.layout = layout()

# Callback pour mettre à jour le contenu du fichier
@app.callback(
    [Output('import-btn', 'disabled'), Output('memories-store', 'data'), Output('alert', 'is_open'), Output('alert', 'children')],
    Input('memories-file-upload', 'contents')
)
def update_file_content(contents):
    if contents is None:
        return True, no_update, no_update, no_update
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        data = json.loads(decoded)
        alert_msg = str(len(data['Saved Media'])) + ' médias trouvés'
        
        return False, data['Saved Media'], True, alert_msg

# Callback pour importer les souvenirs
import time
@app.callback(
    [
        Output('iphone-x', 'children'), 
        Output('memory-id', 'data'), 
        Output('current-memory', 'data'), 
        Output('start-from', 'value'), 
        Output('start-from', 'disabled'), 
        Output('map', 'figure'), 
        Output('memory-date', 'children'),
        Output('alert-danger-import', 'is_open'),
        Output('alert-danger-import', 'children'),
    ],
    [Input('import-btn', 'n_clicks'), Input('import-btn-hidden', 'n_clicks')],    
    [State('memories-store', 'data'), State('memory-id', 'data'), State('start-from', 'value')],
)
def import_memories(n_clicks, hidden_n_clicks, memories, memory_id, start_from):
    
    if n_clicks is not None:

        if os.environ.get('output_path') is None or os.environ.get('temp_path') is None:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, 'Veuillez configurer les variables d\'environnement'

        l = len(memories)

        if len(memories) <= start_from:
            return 'Fin du fichier.', no_update, no_update, no_update, no_update, memory_map(0.0, 0.0), no_update, True, 'Fin du fichier'

        memory = memories[l - start_from - 1]
        download_link = memory['Download Link']

        link = requests.post(download_link)

        ext = '.mp4' if memory['Media Type'] == 'Video' else '.jpg'
        
        path = os.environ.get('temp_path')

        # Supprime tous les fichiers dans le dossier temporaire
        for file in os.listdir(path):
            os.remove(path + file)
        
        fn = path  + memory['Date'][:19].replace(':', '') + ext
        
        downloaded_image_path = download_memory(link.content, fn)

        memories.pop(0)

        # Récupère la latitude et la longitude de memory['Location'] = "Latitude, Longitude: 46.725937, -0.5895955"
        lat, lon = memory['Location'].split(': ')[1].split(', ')
        lat, lon = float(lat), float(lon)

        date = memory['Date'][:10]
        # Formatte en dd/mm/yyyy
        date = date[8:] + '/' + date[5:7] + '/' + date[:4]

        if memory['Media Type'] == 'Video':
            return video(fn), {'id': start_from + 1}, {'name' : fn}, start_from + 1, True, memory_map(lat, lon), date, no_update, no_update
        return picture(fn), {'id': start_from + 1}, {'name' : fn}, start_from + 1, True, memory_map(lat, lon), date, no_update, no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

# Callback pour ajouter un dossier
@app.callback(
    [Output('folder-list', 'children'), Output('alert-warning-add-folder', 'is_open'), Output('alert-warning-add-folder', 'children')],
    [Input('add-folder-btn', 'n_clicks'), Input('url', 'pathname')],
    [State('folder-list', 'children'), State('folder-name', 'value')]
)
def add_folder(n_clicks, url, folder_list, folder_name):
    if callback_context.triggered_id == 'url':
            return load_folders(), no_update, no_update

    if n_clicks:
        fn = folder_name if folder_name else 'Nouveau dossier'

        path = os.environ.get('output_path') + fn + '/'

        if fn in ['.', 'Corbeille']:
            return no_update, True, 'Impossible de créer un dossier avec ce nom'
        
        if os.path.exists(path):
            return no_update, True, 'Un dossier avec ce nom existe déjà'

        folder_list.append(create_folder_item(fn))

        try:
            os.mkdir(path)
        except OSError  as e:
            return no_update, True, e.strerror

        return folder_list, False, no_update
    return no_update, no_update, no_update

# Callback pour gérer les clics sur les dossiers
@app.callback(
    [Output('import-btn-hidden', 'n_clicks'), Output({'type': 'folder-count', 'index': ALL}, 'children'), Output('alert-warning-folder-click', 'is_open'), Output('alert-warning-folder-click', 'children'), Output('folder-tree-disk-usage', 'children')],
    [Input({'type': 'folder-link', 'index': ALL}, 'n_clicks')],
    [
        State('import-btn-hidden', 'n_clicks'),
        State('current-memory', 'data'),
        State({'type': 'folder-count', 'index': ALL}, 'children'),
        State({'type': 'folder-count', 'index': ALL}, 'id'),
        State({'type': 'folder-link', 'index': ALL}, 'id'),
    ],
    prevent_initial_call=True
)
def on_folder_click(n_clicks, n_clicks_hidden, current_memory, count, count_ids, folder_ids):
    ctx = callback_context
    path = os.environ.get('output_path')

    if n_clicks == [] or callback_context.triggered_id['index'] == '.':
        return no_update, [no_update for el in count], no_update, no_update, no_update
    
    elif callback_context.triggered_id['index'] == 'Corbeille':
        try:
            os.remove(current_memory['name'])
        except:
            return no_update, [no_update for el in count], True, 'Impossible de supprimer ce fichier', no_update

        return n_clicks_hidden + 1, count, no_update, no_update, no_update
    else:
        folder_name = ctx.triggered_id['index']
        folder_path = path + folder_name + '/'

        if os.path.exists(folder_path + current_memory['name'].split('/')[-1]):
            return no_update, [no_update for el in count], True, 'Ce fichier existe déjà dans ce dossier'

        os.rename(current_memory['name'], folder_path + current_memory['name'].split('/')[-1])

        for i in range(len(count_ids)):
            if count_ids[i]['index'] == folder_name:
                count[i] = str(os.listdir(folder_path).__len__())
                break

        return n_clicks_hidden + 1, count, no_update, no_update, giga_usage_to_string()

# Fonction pour télécharger un fichier
def download_memory(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None

# Fonction utilitaire pour compter les clics sur les dossiers
def count_clicked_folder(n_clicks):
    sum_click = 0
    for el in n_clicks:
        if el is not None:
            sum_click += el

    return sum_click

# Point d'entrée principal
if __name__ == '__main__':
    app.run(debug=True)
