from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
import base64
from datetime import datetime

@app.route('/drafts')
@role_required('editor')
def draft_page():
    return redirect('/drafts/drafts_news')
    
@app.route('/drafts/drafts_news')
@role_required('editor')
def news_draft_page():
    draft_posts = models.Draft_post.query
    return render_template('/drafts/draft.html', draft_posts = draft_posts)
    
@app.route('/drafts/<nid>')
def news_drafts_full_text_page(nid):
    draft_post = models.Draft_post.query.get_or_404(nid)
    return render_template('drafts/draft_post.html', draft_post=draft_post)
