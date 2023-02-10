from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from spoticloud import get_wordcloud, get_playlist, show_info
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templatesF")
staticfiles = StaticFiles(directory="static")
app.mount("/static", staticfiles, name="static")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Demo"})


@app.post("/playlist")
async def playlist(request: Request, playlist: str = Form(...)):
    playlist = get_playlist(playlist)
    image = get_wordcloud(playlist)
    info = show_info(playlist)
    return templates.TemplateResponse("result.html", {"request": request, "playlist": playlist, 'image': image, 'info': info})


@app.get("/result")
def result(request: Request, playlist: str, image: str, info: str):
    return templates.TemplateResponse("result.html", {"request": request, "playlist": playlist, "image": image, 'info': info})


if __name__ == "__main__":
    uvicorn.run("fast:app", host='127.0.0.1', port=8000, reload=True)