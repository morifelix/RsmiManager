
from decimal import Decimal
from docxtpl import DocxTemplate
from pathlib import Path
from zipfile import ZipFile



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


def create_zip(folder):
    folder=Path(folder)
    zip_path= folder / "temp.zip"

    with ZipFile(zip_path,"w") as zip_file:
        for file in folder.glob("*.docx"):
            zip_file.write(file,arcname=file.name)
    return zip_path
