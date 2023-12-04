from dash import html
import base64

def picture(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    return html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': '100%', 'height': 'auto'})

def video(source):
    with open(source, 'rb') as video_file:
        encoded_video = base64.b64encode(video_file.read()).decode('ascii')
    return html.Div([
        html.Video(src=f'data:video/mp4;base64,{encoded_video}', className='video', controls=True, autoPlay=True)
    ], className='video-container')