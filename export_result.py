import pandas as pd
import numpy as np
import openpyxl
import json
from xlsxwriter.utility import xl_rowcol_to_cell

UPLOADED_FILES_PATH = "uploaded_files/"

def turnOutputIntoExcel(myJsonOutput):
    # print(myJsonOutput)
    # print("DSDJK", type(myJsonOutput))
    myJsonOutput = json.loads((json.dumps(myJsonOutput, ensure_ascii=False)))
    print(type(myJsonOutput))
    # for key, value in myJsonOutput.items():
    #     print(key, value)
    sheet_name = str(myJsonOutput['requestH']['location']).replace('г. Москва, ', '').replace(
            'г. Москва ', '').replace(', д. ', ' ').replace(', ул. ', ' ') + "," + str(myJsonOutput['requestH']['area'])
    
    print(sheet_name)
    outputDataFrameMain = pd.json_normalize(myJsonOutput['requestH'])
    outputDataFrame = pd.json_normalize(
        myJsonOutput, record_path='response')
    req_id = str(outputDataFrame['id'][0])
    print(req_id)
    columns = ['source', 'offer',  'setting', 'area', 'object_type', 'floor', 'floors',
                'location', 'metro_id', 'metro_remoteness', 'rooms',  'material', 'segment',
                'kitchen', 'balcony', 'renovation', 'additions', 'price', 'price_per_metre',
                'price_per_metre_updated', 'all_corrections', 'weight']

    addict = {'source':'avito.ru', 'offer':'Актуально', 'setting':'Жилое помещение (квартира)', 'object_type':'Встроенное помещение', 'additions':'-',
                'metro_id':'metro','price': '', 'price_per_metre':'', 'price_per_metre_updated':'', 'all_corrections':'', 'weight':''}
    

    for j in columns:
        if j not in outputDataFrame.columns.values.tolist():
            outputDataFrame.insert(0, str(j), addict[j])


    for j in columns:
        if j not in outputDataFrameMain.columns.values.tolist():
            if j=='source' or j=='offer':
                outputDataFrameMain.insert(0, str(j), addict['additions'])
            else:
                outputDataFrameMain.insert(0, str(j), addict[j])

    outputDataFrame = pd.concat([outputDataFrameMain, outputDataFrame], axis=0)
    
    new_cols = {'source': 'Источник информации', 'offer': 'Дата предложения',  'setting': 'Назначение',
                            'area': 'Площадь, кв.м.', 'object_type': 'Тип объекта', 'floor': 'Этаж расположения', 'floors': 'Этажность',
                            'location': 'Адрес', 'metro_id': 'Ближайшая ст.метро', 'metro_remoteness': 'Удаленность от метро, мин пешком',
                            'rooms': 'Комнатность',  'material': 'Материал стен', 'segment': 'Сегмент', 'kitchen': 'Площадь кухни, кв.м.',
                            'balcony': 'Наличие балкона/лоджии', 'renovation': 'Состояние отделки', 'additions': 'Дополнительная информация',
                            'price': 'Цена предложения, руб.', 'price_per_metre': 'Цена предложения, руб./кв.м',
                            'price_per_metre_updated': 'Цена предложения с корректировкой, руб./кв.м', 'all_corrections': 'Размер примененных корректировок', 'weight': 'Вес аналога'}
            
    outputDataFrame = outputDataFrame[columns].rename(
        columns=(new_cols)
    ).transpose()
    outputDataFrame.insert(0, 'Элементы сравнения', [x for x in new_cols.values()])
    outputDataFrame.set_axis([f"Аналог №{x-1}" for x in range(0,outputDataFrame.shape[1])], axis='columns', inplace=True)
    outputDataFrame = outputDataFrame.rename(columns = {'Аналог №-1':'Элементы сравнения', 'Аналог №0':'Объект оценки'} )
    
    
    mode="w"
    writer = pd.ExcelWriter(UPLOADED_FILES_PATH+"exp.xlsx", engine='xlsxwriter', mode=mode)
    outputDataFrame.to_excel(writer, index=False, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[f'{sheet_name}']
    worksheet.set_zoom(70)
    header_format = workbook.add_format({
        "valign": "vcenter",
        "align": "center",
        "bg_color": "#A9D08E",
        "bold": True,
        'font_name': 'Segoe UI'
        })
    title = f"Результаты расчёта для {sheet_name}"
    format = workbook.add_format(
        {'font_size': 16,
        'font_name':'Segoe UI',
        'font_color':'#B51F3F'}
    )
    merg_format = workbook.add_format({
        "valign": "vcenter",
        "align": "left",
        "bg_color": "#A9D08E",
        'font_name': 'Segoe UI'
    })

    sub_format = workbook.add_format({
        "valign": "vcenter",
        "align": "left",
        'font_name': 'Segoe UI'
    })
    subheader = f"ID запроса: {req_id}"
    worksheet.merge_range('A1:AS1', title, format)
    
    worksheet.set_row(2, 15)
    
    cell_format = workbook.add_format({"valign": "vcenter", "align": "center"})
    for col_num, value in enumerate(outputDataFrame.columns.values):
        worksheet.write(2, col_num, value, header_format)
    
    worksheet.merge_range('A19:B19', new_cols['price'], merg_format)
    worksheet.merge_range('A20:B20', new_cols['price_per_metre'], merg_format)
    worksheet.merge_range('A21:B21', new_cols['price_per_metre_updated'], merg_format)
    worksheet.merge_range('A22:B22', new_cols['all_corrections'], merg_format)
    worksheet.merge_range('A23:B23', new_cols['weight'], merg_format)
    worksheet.set_column('A:AS', 38, cell_format)
    worksheet.merge_range('A2:AS2', subheader, sub_format)

    workbook.close()

# def turnOutputIntoExcel(myJsonOutput):
#     for i in range(len(myJsonOutput)):
#         print(myJsonOutput)
#         print(type(myJsonOutput))
#         myJsonOutput = json.loads(myJsonOutput)
#         print(type(myJsonOutput))
#         sheet_name = str(myJsonOutput[i]['requestH']['location']).replace('г. Москва, ', '').replace(
#              'г. Москва ', '').replace(', д. ', ' ').replace(', ул. ', ' ') + "," + str(myJsonOutput[i]['requestH']['area'])
        
#         print(sheet_name)
#         outputDataFrameMain = pd.json_normalize(myJsonOutput[i]['requestH'])
#         outputDataFrame = pd.json_normalize(
#             myJsonOutput[i], record_path='response')
#         req_id = str(outputDataFrame['id'][0])
#         print(req_id)
#         columns = ['source', 'offer',  'setting', 'area', 'object_type', 'floor', 'floors',
#                    'location', 'metro_id', 'metro_remoteness', 'rooms',  'material', 'segment',
#                    'kitchen', 'balcony', 'renovation', 'additions', 'price', 'price_per_metre',
#                    'price_per_metre_updated', 'all_corrections', 'weight']

#         addict = {'source':'avito.ru', 'offer':'Актуально', 'setting':'Жилое помещение (квартира)', 'object_type':'Встроенное помещение', 'additions':'-',
#                   'metro_id':'metro','price': '', 'price_per_metre':'', 'price_per_metre_updated':'', 'all_corrections':'', 'weight':''}
        

#         for j in columns:
#             if j not in outputDataFrame.columns.values.tolist():
#                outputDataFrame.insert(0, str(j), addict[j])


#         for j in columns:
#           if j not in outputDataFrameMain.columns.values.tolist():
#                  if j=='source' or j=='offer':
#                    outputDataFrameMain.insert(0, str(j), addict['additions'])
#                  else:
#                    outputDataFrameMain.insert(0, str(j), addict[j])

#         outputDataFrame = pd.concat([outputDataFrameMain, outputDataFrame], axis=0)
        
#         new_cols = {'source': 'Источник информации', 'offer': 'Дата предложения',  'setting': 'Назначение',
#                               'area': 'Площадь, кв.м.', 'object_type': 'Тип объекта', 'floor': 'Этаж расположения', 'floors': 'Этажность',
#                               'location': 'Адрес', 'metro_id': 'Ближайшая ст.метро', 'metro_remoteness': 'Удаленность от метро, мин пешком',
#                               'rooms': 'Комнатность',  'material': 'Материал стен', 'segment': 'Сегмент', 'kitchen': 'Площадь кухни, кв.м.',
#                               'balcony': 'Наличие балкона/лоджии', 'renovation': 'Состояние отделки', 'additions': 'Дополнительная информация',
#                               'price': 'Цена предложения, руб.', 'price_per_metre': 'Цена предложения, руб./кв.м',
#                               'price_per_metre_updated': 'Цена предложения с корректировкой, руб./кв.м', 'all_corrections': 'Размер примененных корректировок', 'weight': 'Вес аналога'}
                
#         outputDataFrame = outputDataFrame[columns].rename(
#             columns=(new_cols)
#         ).transpose()
#         outputDataFrame.insert(0, 'Элементы сравнения', [x for x in new_cols.values()])
#         outputDataFrame.set_axis([f"Аналог №{x-1}" for x in range(0,outputDataFrame.shape[1])], axis='columns', inplace=True)
#         outputDataFrame = outputDataFrame.rename(columns = {'Аналог №-1':'Элементы сравнения', 'Аналог №0':'Объект оценки'} )
        
        
#         if i == 0: 
#         # else: mode="a"
#           mode="w"
#           writer = pd.ExcelWriter(UPLOADED_FILES_PATH+"exp.xlsx", engine='xlsxwriter', mode=mode)
#           outputDataFrame.to_excel(writer, index=False, sheet_name=sheet_name)
#           workbook = writer.book
#           worksheet = writer.sheets[f'{sheet_name}']
#           worksheet.set_zoom(70)
#           header_format = workbook.add_format({
#               "valign": "vcenter",
#               "align": "center",
#               "bg_color": "#A9D08E",
#               "bold": True,
#               'font_name': 'Segoe UI'
#               })
#           title = f"Результаты расчёта для {sheet_name}"
#           format = workbook.add_format(
#               {'font_size': 16,
#                 'font_name':'Segoe UI',
#                 'font_color':'#B51F3F'}
#           )
#           merg_format = workbook.add_format({
#               "valign": "vcenter",
#               "align": "left",
#               "bg_color": "#A9D08E",
#               'font_name': 'Segoe UI'
#           })
        
#           sub_format = workbook.add_format({
#               "valign": "vcenter",
#               "align": "left",
#               'font_name': 'Segoe UI'
#           })
#           subheader = f"ID запроса: {req_id}"
#           worksheet.merge_range('A1:AS1', title, format)
          
#           worksheet.set_row(2, 15)
          
#           cell_format = workbook.add_format({"valign": "vcenter", "align": "center"})
#           for col_num, value in enumerate(outputDataFrame.columns.values):
#               worksheet.write(2, col_num, value, header_format)
            
#           worksheet.merge_range('A19:B19', new_cols['price'], merg_format)
#           worksheet.merge_range('A20:B20', new_cols['price_per_metre'], merg_format)
#           worksheet.merge_range('A21:B21', new_cols['price_per_metre_updated'], merg_format)
#           worksheet.merge_range('A22:B22', new_cols['all_corrections'], merg_format)
#           worksheet.merge_range('A23:B23', new_cols['weight'], merg_format)
#           worksheet.set_column('A:AS', 38, cell_format)
#           worksheet.merge_range('A2:AS2', subheader, sub_format)


#         workbook.close()