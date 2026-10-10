from flask import Blueprint,render_template,request,flash,send_file
from .utils.tra_funcs import *
from .utils.writer_funcs import *
import tempfile
from pathlib import Path

#TODO: add comment here
default_names_json="instance\\agency_names.json"

bp_writer =Blueprint("writer",__name__,template_folder="templates/writer")

@bp_writer.route("/generate",methods=["GET","POST"])
def writer():
    temp_dir=Path(tempfile.mkdtemp())
    def_vals=default_names(default_names_json)

    if request.method =="POST":
        fecha=request.form.get("buwan")
        names=dict(
            agency_name=request.form.get("entity"),
            fund_cluster=request.form.get("fund_cluster"),
            name_supply=request.form.get("officer"),
            name_acc=request.form.get("accounting"),
        )

        for key in names:
            names[key]=names[key].upper()

        lista=ris_sorter(month_setter(fecha))
        rsmiWriter(names,lista,temp_dir)
        zip_path=create_zip(temp_dir)

        return send_file(zip_path,as_attachment=True,download_name=f"{fecha}_RSMI.zip",mimetype="application/zip")

    return render_template("gen.html",**def_vals)


