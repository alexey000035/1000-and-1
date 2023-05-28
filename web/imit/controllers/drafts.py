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
    images = models.Image.query.filter(models.Image.type_post == "draft_post")
    return render_template('/drafts/draft.html', draft_posts = draft_posts, images = images)
    
@app.route('/drafts/<nid>')
def news_drafts_full_text_page(nid):
    draft_post = models.Draft_post.query.get_or_404(nid)
    images = models.Image.query.filter(models.Image.id_post == draft_post.id)
    return render_template('drafts/draft_post.html', draft_post=draft_post, images = images)

@app.route('/drafts/drafts_ads')
@role_required('editor')
def ads_draft_page():
    draft_ads = models.DraftAds.query
    return render_template('/drafts/draft_advert.html', draft_ads = draft_ads)

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

@app.route('/drafts/responderse/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_sug_news(nid):
    edit_form = forms.NewsForm()
    sug_post = models.Sug_post.query.get_or_404(nid).toPost()
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("News with id %s is being edited", nid)
            edit_form.populate_obj(sug_post)
            if edit_form.date.data is not None and edit_form.date.data != "":
                sug_post.date_created = datetime.strptime(edit_form.date.data, "%d.%m.%Y")
            db.session.add(sug_post)
            db.session.commit()

            # Delete cover image if any
            if edit_form.delete_cover_image.data and sug_post.has_cover_image:
                _remove_cover_image(sug_post)
            # Save cover image if any.
            if edit_form.cropped_cover_image_data.data:
                if sug_post.has_cover_image:
                    _remove_cover_image(sug_post)
                if 'full_cover_image' in request.files:
                    file = first(request.files.getlist("full_cover_image"))
                    if file is not None and not file.filename == '':
                        _save_cover_image(edit_form.cropped_cover_image_data.data, file, sug_post)
                    else:
                        app.logger.warning("Cropped image is set but full image is not")
                else:
                    app.logger.warning("Cropped image is set but full image is not")
            return redirect('/drafts/responderse')
        else:
            app.logger.debug("Invalid NewsForm input: {}".format(get_form_errors(edit_form)))
            app.logger.debug("{}".format(first(request.files.getlist("full_cover_image"))))
            flash_errors(edit_form)
    # Passing post data to form fields for editing
    edit_form.title.data = sug_post.title
    edit_form.full_text.data = sug_post.full_text
    return render_template("suggestion_post.html", add_form=edit_form, sug_post=sug_post, add_file_form=forms.FileForm(),
                           edit_file_form=forms.FileEditForm(), remove_file_form=forms.FileRemoveForm())
                           
@app.route('/drafts/responderse/save_drafts/', methods=('GET', 'POST'))
@role_required('editor')
def responderse_save_drafts():
    add_form = forms.NewsForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            post = models.Draft_post()
            add_form.populate_obj(post)
            db.session.add(post)
            db.session.commit()

            # Save cover image if any.
            if add_form.cropped_cover_image_data.data:
                if 'full_cover_image' in request.files:
                    file = first(request.files.getlist("full_cover_image"))
                    if file is not None and not file.filename == '':
                        _save_cover_image(add_form.cropped_cover_image_data.data, file, post)
                    else:
                        print("Cropped image is set but full image is not")
                        app.logger.warning("Cropped image is set but full image is not")
                else:
                    print("Cropped image is set but full image is not")
                    app.logger.warning("Cropped image is set but full image is not")

    return redirect(f'/')
