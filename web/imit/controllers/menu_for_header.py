from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
import base64
from datetime import datetime


items_list = models.Menu.query

def get_items_list():
    return items_list

@app.context_processor
def inject_menu():
    return dict(items_list=items_list)
