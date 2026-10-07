from .models import Transactions,Items
from decimal import Decimal

from docxtpl import DocxTemplate

from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from . import db
from sqlalchemy import select as SELECT
from datetime import date,datetime
from io import BytesIO


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

def batch_setter(fecha:datetime):
    """
    Checks and set the latest RIS no and serial no.
    Args:
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
    This function is used to organize transactions and group simmilar dates to be processed for ris writer.
    """
    transcactions={}
    for item in dbf:
        date=item.date_log
        if not date in transcactions:
            transcactions[date]=[]
        transcactions[date].append(item)
    return transcactions

def rsmiWriter(products:dict):
    saveFolder=os.path.join(targetFolder,f"{tuig}_{buwan}")
    temPlate=r"\static\media\Appendix_64.docx"
    os.makedirs(saveFolder,exist_ok=True)
    for key,vale in products.items():
        doc=DocxTemplate(temPlate)
        items=[]
        curr_ris=None
        for i in vale:
            fecha=i[7]
            total_cost=Decimal(i[3]*i[4])
            formated_tCost=total_cost.quantize(Decimal("0.00"))
            record={"item_code":i[0],"item_name":i[1],"item_type":i[2],"item_used":i[3],"unit_cost":f"{i[4]:,.2f}","total_cost":f"{formated_tCost:,.2f}","object_code":i[5],"ris_no":"-do-" if i[6]==curr_ris else i[6]}
            curr_ris=i[6]
            items.append(record)
        context={"items":items,"serial_no":i[8],"name_supply":"Test I. Nguy","name_acc":"Jan D. Oah","date":fecha.strftime("%d %b %Y")}
        doc.render(context)
        fileName=f"{key}_rsmi.docx"
        doc.save(os.path.join(saveFolder,fileName))
        # print("SAVE",key)
        print(f"Created {fileName} ^_^")
    print("Process Complete xD")