from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
import base64
from datetime import datetime

@app.route('/menu/list')
@role_required('editor')
def menu_list():
    items = models.Menu_items.query
    subitems = models.Menu_subitems.query
    return render_template('menu/menu.html', full=True, items=items, subitems = subitems)
    
@app.route('/menu/add', methods=('GET', 'POST'))
@role_required('editor')
def add_menu():
    add_form = forms.MenuForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            item = models.Menu_items()
            add_form.populate_obj(item)
            db.session.add(item)
            db.session.commit()

            return redirect('/menu/list')
        else:
            app.logger.warning("Invalid MenuForm input: {}".format(get_form_errors(add_form)))
            flash_errors(add_form)
    return render_template("menu/add_menu.html", add_form=add_form)
       
@app.route('/menu/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_menu(nid):
    edit_form = forms.MenuForm()
    item = models.Menu_items.query.get_or_404(nid)
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("Item with id %s is being edited", nid)
            edit_form.populate_obj(item)
            db.session.commit()

            return redirect('/menu/list')
        else:
            app.logger.debug("Invalid MenuForm input: {}".format(get_form_errors(edit_form)))
            flash_errors(edit_form)
    # Passing post data to form fields for editing        
    edit_form.link.data = item.link
    edit_form.name.data = item.name
    edit_form.is_list.data = item.is_list
    return render_template("menu/add_menu.html", add_form=edit_form)
    
@app.route('/menu/<nid>/delete')
@role_required('editor')
def delete_menu_item(nid):
    item = models.Menu_items.query.get_or_404(nid)
    app.logger.debug("Item with id %s is being deleted", nid)
    db.session.delete(item)
    db.session.commit()
    return redirect('/menu/list')
