from imit import app, forms
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
import os
import json
from datetime import datetime

@app.route('/faq')
def faq_page():
    form = forms.FAQFileForm()
    try:
        f = open(os.path.join(app.config["FILE_UPLOAD_PATH"],app.config["FAQ_FILE_NAME"]), 'r')
        js = f.read() #FIXME: use only json module directly?
        js_read = json.loads(js)
        try:
            dt = datetime.strptime(js_read["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
            js_read["date"] = dt.strftime("%d.%m.%Y")
        except Exception:
            js_read["date"] = None
    except Exception:
        app.logger.error("Invalid json input")
        js_read = {}    
    return render_template('faq.html', faq_content=js_read, form=form)

@app.route('/faq/replace_file', methods=['POST'])
@role_required('editor')
def faq_replace_file():
    form = forms.FAQFileForm()
    if form.validate_on_submit():
        app.logger.debug("FAQ file is being replaced")
        ffile = form.file.data
        try:
            filename = os.path.join(app.config["FILE_UPLOAD_PATH"], app.config["FAQ_FILE_NAME"])
            ffile.save(filename)
        except Exception as e:
            app.logger.error('Error during FAQ file replacement', e)
    else:
        app.logger.debug("FAQ file is failed to validate")

    return redirect('/faq')
