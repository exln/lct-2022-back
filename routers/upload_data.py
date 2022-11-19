from fastapi import APIRouter, Depends
from database import *
from utilities import *
from database import get_db
from sqlalchemy.orm import Session
from export_result import turnOutputIntoExcel
import models
import schemas
import oauth2
import uuid
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
import json
from ml import ml_price
from fastapi import FastAPI, Response, status, Depends, Query, File, UploadFile, Form, Body, Request

from typing import Optional, List
from starlette.responses import FileResponse, JSONResponse

router = APIRouter()

UPLOADED_FILES_PATH = "uploaded_files/"


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file(response: Response, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Format new filename
    full_name = format_filename(file)

    # Save file
    await save_file_to_uploads(file, full_name)

    # Get file size
    file_size = get_file_size(full_name)

    # async def get_current_id(id: uuid = Depends(db)):
    #     file_id = id
    #     return file_id

    # Add to DB

    response.status_code = status.HTTP_201_CREATED
    file_id = add_file_to_db(
        db,
        full_name=full_name,
        file_size=file_size,
        file=file
    )

    # Get info from DB
    file_info_from_db = get_file_from_db_from_id(db, file_id)
    print(file_id)
    return {'fileid': file_info_from_db.id}


@router.get('/{id}')
def get_upload(id: uuid.UUID, db: Session = Depends(get_db)):
    print(id)
    file_info_from_db = get_file_from_db_from_id(db, id)

    return JSONResponse(json_file_from_excel(
        db,
        id=file_info_from_db.id
    ))


@router.get("/requests/all")
async def read_user_requests(skip: int = 0, limit: int | None = None, db: Session = Depends(get_db)):
    resp = []
    user_id = '139837b5-d37a-4d2c-8525-23d7d2af7eac'
    requests = get_file_from_db_from_user(db, user_id)
    for request in requests:
        item = {"request_id": request.id, "created_at": request.created_at}
        resp.append(item)
    return resp


@router.post('/{id}/calculate_data')
async def calculate_data(requests: List[schemas.FlatSchema], id: uuid.UUID):
    return ResultOfCalcs(jsonable_encoder(requests))


@router.post("/{id}/download", status_code=status.HTTP_200_OK)
async def turn_My_Output_Into_Excel(
    id: uuid.UUID,
    payload: list = Body(...),
):
    turnOutputIntoExcel(payload[0])
    return FileResponse(UPLOADED_FILES_PATH+"exp.xlsx", filename="export.xlsx")


@router.post("/{id}/machine", status_code=status.HTTP_200_OK)
async def show_machine_price(id: uuid.UUID,
    payload: list = Body(...)):
    return ml_price(jsonable_encoder(payload))
