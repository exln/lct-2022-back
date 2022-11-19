import io
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from passlib.context import CryptContext  # type: ignore
from ml import ml_price
import models
from coordinates import GetAddress, GetCords, GetDistanceBetween
from corrections import resultOFCorr, summOFCorr, summOFCorrWithoutRenovation

UPLOADED_FILES_PATH = "uploaded_files/"
SOURCE_FILES_PATH = "sources/"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def format_filename(file):

    filename, ext = os.path.splitext(file.filename)
    date = str(datetime.now().time().strftime("%H-%M-%S"))[:-3]

    return filename + '-' + date + ext


async def save_file_to_uploads(file, filename):
    with open(f'{UPLOADED_FILES_PATH}{filename}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()


def get_file_size(filename, path: str = None):
    file_path = f'{UPLOADED_FILES_PATH}{filename}'
    if path:
        file_path = f'{path}{filename}'
    return os.path.getsize(file_path)


def get_file_from_db(db):
    return db.query(models.UserRequest).first()


def get_file_from_db_from_id(db, id):
    return db.query(models.UserRequest).filter(models.UserRequest.id == id).first()


def get_requests_count(db, user_id):
    return get_file_from_db_from_user(db, user_id).count()


def get_file_from_db_from_user(db, user_id):
    print(db.query(models.UserRequest).filter(
        models.UserRequest.user_id == user_id))
    return db.query(models.UserRequest).filter(models.UserRequest.user_id == user_id)


def add_file_to_db(db, **kwargs):
    new_file = models.UserRequest(
        name=kwargs['full_name'],
        size=kwargs['file_size'],
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file.id


def delete_file_from_uploads(file_name):
    try:
        os.remove(UPLOADED_FILES_PATH + file_name)
    except Exception:
        print(Exception)


def update_file_in_db(db, **kwargs):
    update_file = db.query(models.UserRequest).first()
    # update_file = db.query(models.UserRequest).filter(models.UserRequest.id == kwargs['id']).first()
    update_file.name = kwargs['full_name']
    update_file.size = kwargs['file_size']

    update_file.modification_time = datetime.now()
    db.commit()
    db.refresh(update_file)
    return "Done"


def json_file_from_excel(db, **kwargs):
    data = pd.read_excel(
        f'uploaded_files/{db.query(models.UserRequest).filter(models.UserRequest.id == kwargs["id"]).first().name}', skiprows=0, usecols='A:K')
    # print(kwargs['id'])
    data.rename(
        columns=({'Количество комнат': 'rooms', 'Материал стен (Кипич, панель, монолит)': 'material', 'Местоположение': 'location',
                  'Наличие балкона/лоджии': 'balcony', 'Площадь квартиры, кв.м': 'area', 'Площадь кухни, кв.м': 'kitchen', 'Сегмент (Новостройка, современное жилье, старый жилой фонд)': 'segment',
                  'Состояние (без отделки, муниципальный ремонт, с современная отделка)': 'renovation', 'Удаленность от станции метро, мин. пешком': 'metro_remoteness', 'Этаж расположения': 'floor', 'Этажность дома': 'floors'}), inplace=True)

    data.insert(0, 'id', list(np.arange(0, data.shape[0])))

    json_str = data.to_json(force_ascii=False, orient='records')

    # json_data = json.dumps(json_str)
    json_without_slash = json.loads(json_str)
    return json_without_slash


def AddResult(requestDataFrame, responseDataFrame, result_dict):
    requestsDict = [{k: v for k, v in x.items() if pd.notnull(v)}
                    for x in requestDataFrame.to_dict(orient='records')]
    responsesDict = [{k: v for k, v in x.items() if pd.notnull(v)}
                     for x in responseDataFrame.to_dict(orient='records')]
    requestsDictUpd = requestsDict[0]
    requestsDictUpd['mlPrice'] = int(ml_price(requestsDictUpd))
    result = {'requestH': requestsDictUpd, 'response': responsesDict}
    print(result)
    print(type(result))
    result_dict.append(result)
    return result_dict


def JsonResultOfCalcs(result_dict):
    json_result = json.dumps(result_dict, ensure_ascii=False)
    json_without_slash = json.loads(json_result)
    print(type(json_without_slash))
    return json_without_slash


def ResultOfCalcs(myJsonRequest):
    requestDataFrame = pd.json_normalize(myJsonRequest)
    analogsDataFrame = pd.read_csv(SOURCE_FILES_PATH+'analogs-db.csv', encoding='cp1251')
    workDataFrame = analogsDataFrame.copy()
    workDataFrame = workDataFrame.drop(
        ['source', 'offer', 'setting', 'object_type', 'additions'], axis=1)
    requestDataFrame.insert(1, 'latitude', list([GetCords(requestDataFrame['location'][i].replace('г. ', '').replace(
        ', д. ', ', ').replace('город', '')).cords.latitude for i in range(len(requestDataFrame['location']))]))
    requestDataFrame.insert(2, 'longitude', list([GetCords(requestDataFrame['location'][i].replace('г. ', '').replace(
        ', д. ', ', ').replace('город', '')).cords.longitude for i in range(len(requestDataFrame['location']))]))

    responseDataFrame = pd.DataFrame()
    result_dict = []
    for i in range(len(requestDataFrame['id'])):
        listTorg, listFloor, listArea, listKitchen, listBalcony, listMetro, listRenovation, listAds = [
        ], [], [], [], [], [], [], []
        listPriceUpdated, listCorrectionsAll = [], []
        responseDataFrame = pd.DataFrame()
        locationFrom = f"{requestDataFrame['latitude'][i]},{requestDataFrame['longitude'][i]}"
        for j in range(len(workDataFrame['id'])):
            if (str(requestDataFrame['rooms'][i]) == str(workDataFrame['rooms'][j] or (requestDataFrame['rooms'][i]=="Студия" and workDataFrame['rooms'][j]=="студия")) and GetDistanceBetween(locationFrom, f"{workDataFrame['latitude'][j]},{workDataFrame['longitude'][j]}").distance <= 1.0):
                corrections = summOFCorrWithoutRenovation(requestDataFrame['floor'][i], workDataFrame['floor'][j], requestDataFrame['floors'][i], workDataFrame['floors'][j], requestDataFrame['area'][i], workDataFrame['area'][j], requestDataFrame['kitchen']
                                                          [i], workDataFrame['kitchen'][j], requestDataFrame['balcony'][i], workDataFrame['balcony'][j], requestDataFrame['metro_remoteness'][i], workDataFrame['metro_remoteness'][j], requestDataFrame['renovation'][i], workDataFrame['renovation'][j])

                corrections = [1 if v is None else v for v in corrections]

                listTorg.append(corrections[0])
                listFloor.append(corrections[1])
                listArea.append(corrections[2])
                listKitchen.append(corrections[3])
                listBalcony.append(corrections[4])
                listMetro.append(corrections[5])
                listRenovation.append(corrections[6])

                listPriceUpdated.append(resultOFCorr(
                    workDataFrame['price_per_metre'][j], corrections))
                listCorrectionsAll.append(summOFCorr(
                    workDataFrame['price_per_metre'][j], corrections))
                address = GetAddress(
                    f"{workDataFrame['latitude'][j]},{workDataFrame['longitude'][j]}").raw_address
                element = [address['address']['city'] if 'city' in address['address']
                           else (address['address']['village'] if 'village' in address['address']
                                 else(address['address']['town'] if 'town' in address['address'] else '')),
                           address['address']['road'] if 'road' in address['address'] else '',
                           address['address']['house_number'] if 'house_number' in address['address'] else '']

                listAds.append((', ').join(str(x) for x in list(element)))
                responseDataFrame = pd.concat(
                    [responseDataFrame, workDataFrame.iloc[[j]]])
        responseDataFrame.insert(0, 'torgCorr', listTorg)
        responseDataFrame.insert(0, 'floorCorr', listFloor)
        responseDataFrame.insert(0, 'areaCorr', listArea)
        responseDataFrame.insert(0, 'kitchenCorr', listKitchen)
        responseDataFrame.insert(0, 'balconyCorr', listBalcony)
        responseDataFrame.insert(0, 'metroCorr', listMetro)
        responseDataFrame.insert(0, 'renovationCorr', listRenovation)
        responseDataFrame.insert(
            0, 'price_per_metre_updated', listPriceUpdated)
        responseDataFrame.insert(0, 'all_corrections', listCorrectionsAll)
        responseDataFrame.insert(2, 'location', listAds)

        buff = 0
        for a in range(len(listCorrectionsAll)):
            buff += (1/listCorrectionsAll[a])

        responseDataFrame.insert(0, 'weight', list(
            [((1/listCorrectionsAll[x])/(buff)) if x > 0 else 0 for x in range(len(listCorrectionsAll))]))

        AddResult(requestDataFrame.iloc[[i]], responseDataFrame, result_dict)

    return JsonResultOfCalcs(result_dict)
