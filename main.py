from distutils.command.upload import upload
from fastapi import FastAPI
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import routers.auth as auth
import routers.upload_data as upload_data
import routers.user as user
# import routers.export_data as export_data
# import routers.import_data as import_data
import uvicorn
import gunicorn

app = FastAPI(
    title="EXILON-API",
    description="""
    Решение кейса №6.
    Подробная документация: https://clck.ru/32b4zJ
    """,
    version="0.1",
    docs_url="/api/documentation"
)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "The login logic.",
    },
    {
        "name": "User",
        "description": "User personal account page.",
    },
    {
        "name": "Upload",
        "description": "Upload your raw data.",
    },
    {
        "name": "Import",
        "description": "Import the handled data.",
    },
    {
        "name": "Export",
        "description": "Export the handled data.",
    },
]


origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Authentication'], prefix='/api/auth')
app.include_router(user.router, tags=['User'], prefix='/api/user')
app.include_router(upload_data.router, tags=['Upload'], prefix='/api/data')
# app.include_router(import_data.router, tags=['Import'], prefix='/api/import')
# app.include_router(export_data.router, tags=['Export'], prefix='/api/export')


@app.get('/api')
def root():
    return {'message': 'Привет, используй этот адрес для обращения к API (swagger: /api/documentation'}


if __name__ == "__main__":
    gunicorn.run(app, host="0.0.0.0", port=8000)
