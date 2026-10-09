from .models import Transactions,Items
from decimal import Decimal

from docxtpl import DocxTemplate

from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from . import db
from sqlalchemy import select as SELECT
from datetime import date,datetime
from pathlib import Path
from zipfile import ZipFile
import json



def default_names(filepath:str):
    try:
        with open(filepath,"r") as f:
            values =json.load(f)
        return dict(values)
    except:
        values={
            "entity":"Agency Name Here",
            "fund_cluster":"Regular Funds",
            "officer":"Cheezit U. Piattos",
            "accounting":"Chippy H. Nova"
                }
        return values


def month_setter(fecha,batch_max=False):
    """Dynamic query for the database of a selected month, returns an sequence or tuple. ADD MORE DETAILS LATER!
    Args:
        fecha: Only accepts Year & Month as strings i.e. '%Y-%m'.
        batch_max: insert explaination here later.
    Returns: 
        sequence: Transactions filtered by the selected month.
    """
    buwan=date.fromisoformat(fecha+"-01")
    querying=(SELECT(Transactions).join(Items)).where(Transactions.date_log >= buwan ,Transactions.date_log <buwan + relativedelta(months=1))
    querying2=(SELECT(func.max(Transactions.date_log),func.max(Transactions.batch_no),func.max(Transactions.serial_no))).where(Transactions.date_log >= buwan ,Transactions.date_log <buwan + relativedelta(months=1))
    lista=db.session.scalars(querying).all() if not batch_max else db.session.execute(querying2).one()
    return lista

def batch_setter(fecha:datetime)-> tuple:
    """
    Checks and set the latest RIS no and serial no.
    Args:
        fecha (datetime): Date to check and compare to update the serial number.

    Returns: (tuple) Returns Tuple of RIS NO, then SERIAL number.
    """
    tuig=fecha.year
    buwan=fecha.month
    lista=month_setter(fecha.strftime("%Y-%m"),True)

    try:
        risCount=int(lista[1].split("-")[2])
        ultimaDay= lista[0].day
        cereal_count= int(lista[2].split("-")[2])
    except AttributeError:
        risCount=0
        ultimaDay=0
        cereal_count=0
    
    if ultimaDay !=fecha.day:
        cereal_count +=1

    risCount +=1
    
    newCereal=f"{tuig}-{buwan:02d}-{(cereal_count):03d}"
    newRis=f"{tuig}-{buwan:02d}-{(risCount):03d}"

    return (newRis,newCereal)



def ris_sorter(dbf)->dict:
    """
    To organize transactions and group simmilar dates to be processed for ris writer.
    """
    transcactions={}
    for item in dbf:
        date=item.date_log
        if not date in transcactions:
            transcactions[date]=[]
        transcactions[date].append(item)
    return transcactions

def rsmiWriter(details:dict,lista:dict,output:str) -> None:
    """
    This will create RIS documents by selected month and saves them to a target folder.

    Args:
        details (dict): A dictionary containing the vales for agency, fundcluster,supply officer, accountant.
        lista (dict): A dictionary organized into dates which should be processed and made by ris_sorter.
        output (str): The directory path that where the writer would save the documents.
    """
    saveFolder=Path(output)
    temPlate="src\\static\\media\\Appendix_64.docx"
    for key,vale in lista.items():
        doc=DocxTemplate(temPlate)
        items=[]
        curr_ris=None
        for i in vale:
            fecha=i.date_log
            total_cost=Decimal(i.items_used*i.items.unit_cost)
            formated_tCost=total_cost.quantize(Decimal("0.00"))
            record={"item_code":i.item_id,"item_name":i.items.item_name,"item_type":i.items.unit_type,"item_used":i.items_used,"unit_cost":f"{i.items.unit_cost:,.2f}","total_cost":f"{formated_tCost:,.2f}","object_code":i.items.uacs_code,"ris_no":"-do-" if i.batch_no==curr_ris else i.batch_no}
            curr_ris=i.batch_no
            items.append(record)
        context={"items":items,"serial_no":i.serial_no,"date":fecha.strftime("%d %b %Y")}
        context.update(details)
        doc.render(context)
        fileName=f"{key}_rsmi.docx"
        doc.save(saveFolder / fileName)
        print(f"Created {fileName} ^_^")
    print("Process Complete xD")


def create_zip(folder,file_name):
    folder=Path(folder)
    zip_path= folder / f"{file_name}.zip"

    with ZipFile(zip_path,"w") as zip_file:
        for file in folder.glob("*.docx"):
            zip_file.write(file,arcname=file.name)
    return zip_path
