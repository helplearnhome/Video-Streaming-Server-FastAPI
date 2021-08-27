# fastapi_app.py 
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates

from web_cam import Camera 

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
'''
This is a HTML Response. Which has the html template to play the stream.
'''
async def index(request: Request):
   return templates.TemplateResponse('index.html', {"request": request})

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    '''
    You can get the streamed data by a get request of media type multipart/x-mixed-replace and boundary=frame
    '''
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(Camera()),media_type='multipart/x-mixed-replace; boundary=frame')

