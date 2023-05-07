from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
import base64
from datetime import datetime


@app.route('/adverts')
def ads_page():
    try:
        year = int(request.args.get("year", datetime.now().year))
        end_year = datetime.strptime(str(year + 1), "%Y")
        year = datetime.strptime(str(year), "%Y")
        year_selected = True
    except ValueError:
        year = datetime.strptime("2016", "%Y")
        end_year = datetime.now()
        year_selected = False
    
    years = range(2016, datetime.now().year + 1)
    pages = models.Ads.query.filter(models.Ads.date_created.between(year, end_year)) \
       .order_by(desc(models.Ads.date_created))
    return render_template('ads/ads_list.html', full=True, ads=pages, cur_year=year.year, years=years, year_selected=year_selected)

@app.route('/ads/add', methods=('GET', 'POST'))
@role_required('editor')
def add_ads(): 	
    add_form = forms.AdsForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            advert = models.Ads()
            add_form.populate_obj(advert)
            if add_form.date.data is not None and add_form.date.data != "":
               	advert.date_created = datetime.strptime(add_form.date.data, "%Y.%m.%n")          
            db.session.add(advert)
            db.session.commit()
            return redirect('/')
            
        else:
            app.logger.warning("Invalid NewsForm input: {}".format(get_form_errors(add_form)))
       	    flash_errors(add_form)
    return render_template("ads/add_ads.html", add_form=add_form)

@app.route('/ads/add/save', methods=('GET', 'POST'))
@role_required('editor')
def add_ads_save():
    add_form = forms.DraftAdsForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            advert = models.DraftAds()
            add_form.populate_obj(advert)

            db.session.add(advert)
            db.session.commit()

    return redirect(f'/')



@app.route('/ads/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_ads(nid):
    edit_form = forms.AdsForm()
    advert = models.Ads.query.get_or_404(nid)
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("Ads with id %s is being edited", nid)
            edit_form.populate_obj(advert)
            db.session.commit()
            return redirect('/')
            
        else:
            app.logger.debug("Invalid AdsForm input: {}".format(get_form_errors(edit_form)))
            flash_errors(edit_form)
    # Passing post data to form fields for editing        
    edit_form.description.data = advert.description
    return render_template("ads/add_ads.html", add_form=edit_form, advert=advert)



@app.route('/ads/<nid>/delete')
@role_required('editor')
def delete_ads(nid):
    advert = models.Ads.query.get_or_404(nid)
    app.logger.debug("Ads with id %s is being deleted", nid)

    db.session.delete(advert)
    db.session.commit()
    return redirect('/')



@app.route('/drafts_ads/<nid>/delete')
@role_required('editor')
def delete_draft_ads(nid):
    advert = models.DraftAds.query.get_or_404(nid)
    app.logger.debug("Ads with id %s is being deleted", nid)
    db.session.delete(advert)
    db.session.commit()
    return redirect('/drafts/drafts_ads')


@app.route('/drafts_ads/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_draft_ads(nid):
    edit_form = forms.AdsForm()
    advert = models.DraftAds.query.get_or_404(nid).toAds()
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("Ads with id %s is being edited", nid)
            edit_form.populate_obj(advert)
            if edit_form.date.data is not None and edit_form.date.data != "":
                advert.date_created = datetime.strptime(edit_form.date.data, "%d.%m.%Y")
            db.session.add(advert)
            db.session.commit()
           
            return redirect('/')
        else:
            app.logger.debug("Invalid NewsForm input: {}".format(get_form_errors(edit_form)))
            flash_errors(edit_form)
    # Passing post data to form fields for editing
    edit_form.description.data = advert.description
    return render_template("ads/add_ads.html", add_form=edit_form, advert = advert)



