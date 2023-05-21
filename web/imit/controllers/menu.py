from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc, func
import base64
from datetime import datetime

@app.route('/menu/list')
@role_required('editor')
def menu_list():
    items = models.Menu.query
    return render_template('menu/menu.html', full=True, items=items)
    
@app.route('/menu/add', methods=('GET', 'POST'))
@role_required('editor')
def add_menu():
    add_form = forms.MenuForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            item = models.Menu()
            if add_form.father.data is None or add_form.father.data != "":
                u = models.Menu.query.filter_by(name=add_form.father.data).first()
                item.father_id = u.id
            add_form.populate_obj(item)
            
            menu_items = models.Menu.query.filter_by(father_id=item.father_id)
            x = 0
            for menu_item in menu_items:
                print (menu_item.name)
                if menu_item.number > x:
                    x = menu_item.number
            item.number = x + 1
            
            db.session.add(item)
            db.session.commit()
            return redirect('/menu/list')
        else:
            app.logger.warning("Invalid MenuForm input: {}".format(get_form_errors(add_form)))
            flash_errors(add_form)
    return render_template("menu/add_menu.html", add_form=add_form)
    
@app.route('/menu/<nid>/delete')
@role_required('editor')
def delete_menu_item(nid):
    item = models.Menu.query.get_or_404(nid)
    app.logger.debug("Item with id %s is being deleted", nid)
    db.session.delete(item)
    db.session.commit()
    return redirect('/menu/list')
    
@app.route('/menu/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_menu(nid):
    edit_form = forms.MenuForm()
    item = models.Menu.query.get_or_404(nid)
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("Item with id %s is being edited", nid)
            edit_form.populate_obj(item)
            
            menu_items = models.Menu.query.filter_by(father_id=item.father_id)
            for menu_item in menu_items: 
                if menu_item.number >= item.number and menu_item.id != item.id:
                    menu_item.number += 1
            
            
            db.session.commit()
            return redirect('/menu/list')
        else:
            app.logger.debug("Invalid MenuForm input: {}".format(get_form_errors(edit_form)))
            flash_errors(edit_form)
    # Passing post data to form fields for editing        
    edit_form.link.data = item.link
    edit_form.name.data = item.name
    edit_form.size.data = item.size
    edit_form.number.data = item.number
    if item.father_id is not None:
        u = models.Menu.query.filter_by(id=item.father_id).first()
        edit_form.father.data = u.name
    return render_template("menu/add_menu.html", add_form=edit_form)
