from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import shutil

def folder_tree_panel():
    return dbc.Card(
        [
            dbc.CardHeader(['Arborescence des dossiers', html.Span(giga_usage_to_string(), id='folder-tree-disk-usage', className='float-right')], className='d-flex justify-content-between align-items-center'),
            dbc.CardBody(
                [
                    dbc.ListGroup(    
                        load_folders(),
                        id="folder-list",
                    ),
                    # text for folder name
                    html.Div(
                        children = [
                            dbc.Input(id="folder-name", placeholder="Nom du dossier", type="text", className="mt-2"),
                            dbc.Button(html.I(className="fas fa-add"), id="add-folder-btn", color="primary", className="mt-2"),  
                        ],
                        id="add-folder-content"
                    )
                    
                ]
            ),
        ],
        id='folder-tree-panel'
    )

# Function to create a folder item
def create_folder_item(folder_name, is_hidden=False, folder_count=0):
    return dbc.ListGroupItem(
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.I(className="fas fa-folder"), width=1),
                    dbc.Col(folder_name, width=10),
                    dbc.Col(html.Span(folder_count, id={"type": "folder-count", "index": folder_name})),
                ],
                align="center",
            ),
            id={"type": "folder-link", "index": folder_name},
            href="#",
            className="folder-item",
        ),
        style={"display": "none"} if is_hidden else {},
    )

def load_folders():
    path = os.environ.get('output_path')
    folders = os.listdir(path)

    folder_list = [create_folder_item('.'),create_folder_item('Corbeille')]
    for folder in folders:

        # count number of files in folder
        number_of_files = len(os.listdir(path + folder))

        folder_list.append(create_folder_item(folder, folder_count=number_of_files))

    return folder_list

def giga_usage_to_string():
    path = os.environ.get('output_path')
    
    # get folder size
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))

    # convert to Mo
    total_size = total_size / 1000000000

    if total_size < 1:
        return str(round(total_size * 1000, 2)) + ' Mo'

    return str(round(total_size, 2)) + ' Go'