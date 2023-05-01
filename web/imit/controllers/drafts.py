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

@app.route('/drafts/responderse')
@role_required('editor')
def sug_news_draft_page():
    try:
        year = int(request.args.get("year", datetime.now().year))
        end_year = datetime.strptime(str(year + 1), "%Y")
        year = datetime.strptime(str(year), "%Y")
        year_selected = True
    except ValueError:
        year = datetime.strptime("2016", "%Y")
        end_year = datetime.now()
        year_selected = False
    sug_posts = models.Sug_post.query.filter(models.Sug_post.date_created.between(year, end_year)) \
        .order_by(desc(models.Sug_post.date_created))
    return render_template('drafts/draft_suggestion.html', sug_posts = sug_posts)
    
@app.route('/drafts/responderse/<nid>')
@role_required('editor')
def sug_news_full_text_page(nid):
    sug_post = models.Sug_post.query.get_or_404(nid)
    return render_template('drafts/sug_post.html', sug_post=sug_post)
    
@app.route('/drafts/responderse/<nid>/delete')
@role_required('editor')
def delete_sug_news(nid):
    sug_post = models.Sug_post.query.get_or_404(nid)
    app.logger.debug("News with id %s is being deleted", nid)
    # for file in post.files:
    #     if not remove_file(file):
    #         return "Ошибка при удалении файла"
    # # Delete cover image
    # if post.has_cover_image:
    #     _remove_cover_image(post)
    db.session.delete(sug_post)
    db.session.commit()
    return redirect('/drafts/responderse')
