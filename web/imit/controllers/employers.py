from imit import app, models, forms, db
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, remove_file, first
from flask import render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
import base64
from datetime import datetime

@app.route('/employers')
def employers_page():
    employers = models.Employers.query.all()
    return render_template('employers/employers.html', employers = employers)
    
    

@app.route('/employers/<nid>')
def employer_page(nid):
    employer = models.Employers.query.get_or_404(nid)
    return render_template('employers/employer.html', employer=employer)
    

@app.route('/employers/add', methods=('GET', 'POST'))
@role_required('editor')
def add_employers():
    add_form = forms.EmployersForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            employer = models.Employers()
            add_form.populate_obj(employer)
            db.session.add(employer)
            db.session.commit()

            # Save cover image if any.
            if add_form.cropped_cover_image_data.data:
                if 'full_cover_image' in request.files:
                    file = first(request.files.getlist("full_cover_image"))
                    if file is not None and not file.filename == '':
                        _save_cover_image(add_form.cropped_cover_image_data.data, file, employer)
                    else:
                        print("Cropped image is set but full image is not")
                        app.logger.warning("Cropped image is set but full image is not")
                else:
                    print("Cropped image is set but full image is not")
                    app.logger.warning("Cropped image is set but full image is not")

            return redirect(f'/employers/{employer.id}')
        else:
            app.logger.warning(f"Invalid NewsForm input: {get_form_errors(add_form)}")
            flash_errors(add_form)

    return render_template("employers/add_employer.html",
                           add_form=add_form,
                           add_file_form=forms.FileForm(),
                           edit_file_form=forms.FileEditForm(),
                           remove_file_form=forms.FileRemoveForm()
                           )

@app.route('/employers/<nid>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_employers(nid):
    edit_form = forms.EmployersForm()
    employer = models.Employers.query.get_or_404(nid)
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("News with id %s is being edited", nid)
            edit_form.populate_obj(employer)

            db.session.commit()

            # Delete cover image if any
            if edit_form.delete_cover_image.data and employer.has_cover_image:
                _remove_cover_image(employer)
            # Save cover image if any.
            if edit_form.cropped_cover_image_data.data:
                if employer.has_cover_image:
                    _remove_cover_image(employer)
                if 'full_cover_image' in request.files:
                    file = first(request.files.getlist("full_cover_image"))
                    if file is not None and not file.filename == '':
                        _save_cover_image(edit_form.cropped_cover_image_data.data, file, employer)
                    else:
                        app.logger.warning("Cropped image is set but full image is not")
                else:
                    app.logger.warning("Cropped image is set but full image is not")
            return redirect('/employers')
            #return redirect('/employers/{}'.format(employer.id))
        else:
            app.logger.debug("Invalid NewsForm input: {}".format(get_form_errors(edit_form)))
            app.logger.debug("{}".format(first(request.files.getlist("full_cover_image"))))
            flash_errors(edit_form)
    # Passing post data to form fields for editing        
    edit_form.name.data = employer.name
    edit_form.logo.data = employer.logo
    edit_form.link.data = employer.link
    edit_form.promo_link.data = employer.promo_link
    edit_form.date.data = employer.date
    edit_form.desc_company.data = employer.desc_company
    return render_template("employers/add_employer.html", add_form=edit_form, employer=employer, add_file_form=forms.FileForm(),
                           edit_file_form=forms.FileEditForm(), remove_file_form=forms.FileRemoveForm())


@app.route('/employers/<nid>/delete')
@role_required('editor')
def delete_employers(nid):
    employer = models.Employers.query.get_or_404(nid)
    app.logger.debug("News with id %s is being deleted", nid)

    # Delete cover image
    if employer.has_cover_image:
        _remove_cover_image(employer)
    db.session.delete(employer)
    db.session.commit()
    return redirect('/employers')


def _save_cover_image(data, full_file, employer):
    app.logger.debug("Adding cover image to news %s", employer.id)
    if data is None or employer is None:
        app.logger.error("None is not accepted")
        return False
    filename = secure_filename("ci_{}.png".format(employer.id))
    fn, file_extension = os.path.splitext(full_file.filename)
    full_filename = secure_filename("ci_{}_full{}".format(employer.id, file_extension))
    try:
        app.logger.debug("Storing images %s and %s to drive", filename, full_filename)
        with open(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", filename), "wb") as fh:
            fh.write(base64.b64decode(data.split(",")[1]))
        full_file.save(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", full_filename))
    except Exception as e:
        app.logger.error('Error ocurried during cover image file saving: %s', e)
        return False
    employer.cover_image = full_filename
    db.session.commit()
    return True


def _remove_cover_image(employer):
    try:
        os.remove(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", employer.cover_image))
        os.remove(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", "ci_{}.png".format(employer.id)))
    except Exception as e:
        app.logger.error('Error occurred during cover image deletion: %s', e)
        return False
    employer.cover_image = None
    db.session.commit()
    return True


