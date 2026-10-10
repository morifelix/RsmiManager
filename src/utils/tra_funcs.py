from .models import Transactions,Items

from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from src import db
from sqlalchemy import select as SELECT
from datetime import date,datetime

import json


#TODO: Add comment here
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



