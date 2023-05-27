from flask import abort
from imit import app, models, forms, db, babel
import imit.utils as utils
from imit.utils import role_required, flash_errors, get_form_errors, first
from flask import render_template, request, redirect, make_response, g, jsonify, flash
import flask_login
from sqlalchemy import desc, asc
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import base64

@app.route('/')
def index_page():
    year = datetime.strptime(str(datetime.now().year), "%Y")
    end_year = datetime.strptime(str(datetime.now().year + 1), "%Y")

    years = range(2016, datetime.now().year + 1)
    pages = models.Post.query.filter(models.Post.date_created.between(year, end_year)) \
        .order_by(desc(models.Post.date_created))
    pages_ads = models.Ads.query.filter(models.Ads.date_created.between(year, end_year)) \
        .order_by(desc(models.Ads.date_created))
    images = models.Image.query.filter(models.Image.type_post == "post")
    return render_template('index.html', full=False, posts=pages, ads=pages_ads, cur_year=year.year, years=years, year_selected=True, images = images)


@app.route('/about')
def about_page():
    return render_template('about.html', active_page="about")


@app.route('/news/suggestion', methods=('GET', 'POST'))
def sug_news():
    add_form = forms.NewsForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            sug_post = models.Sug_post()
            add_form.populate_obj(sug_post)
            if add_form.date.data:
                sug_post.date_created = datetime.strptime(add_form.date.data, "%d.%m.%Y")
            db.session.add(sug_post)
            db.session.commit()

            # Save cover image if any.
            if add_form.cropped_cover_image_data.data:
                if 'full_cover_image' in request.files:
                    file = first(request.files.getlist("full_cover_image"))
                    if file is not None and not file.filename == '':
                        _save_cover_image(add_form.cropped_cover_image_data.data, file, sug_post)
                    else:
                        print("Cropped image is set but full image is not")
                        app.logger.warning("Cropped image is set but full image is not")
                else:
                    print("Cropped image is set but full image is not")
                    app.logger.warning("Cropped image is set but full image is not")

            return redirect('/')
        else:
            app.logger.warning(f"Invalid NewsForm input: {get_form_errors(add_form)}")
            flash_errors(add_form)

    return render_template("suggestion_post.html",
                           add_form=add_form,
                           add_file_form=forms.FileForm(),
                           edit_file_form=forms.FileEditForm(),
                           remove_file_form=forms.FileRemoveForm()
                           )

def _save_cover_image(data, full_file, sug_post):
    app.logger.debug("Adding cover image to sug_news %s", sug_post.id)
    if data is None or sug_post is None:
        app.logger.error("None is not accepted")
        return False
    filename = secure_filename("ci_{}.png".format(sug_post.id))
    fn, file_extension = os.path.splitext(full_file.filename)
    full_filename = secure_filename("ci_{}_full{}".format(sug_post.id, file_extension))
    try:
        app.logger.debug("Storing images %s and %s to drive", filename, full_filename)
        with open(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", filename), "wb") as fh:
            fh.write(base64.b64decode(data.split(",")[1]))
        full_file.save(os.path.join(app.config['FILE_UPLOAD_PATH'], "covers", full_filename))
    except Exception as e:
        app.logger.error('Error ocurried during cover image file saving: %s', e)
        return False
    sug_post.cover_image = full_filename
    db.session.commit()
    return True

@app.route('/new_header')
def test_page():
    return render_template('test.html', active_page="about")

@app.route('/employers_test')
def employers_test_page():
    return render_template('employers_test.html', active_page="about")

@app.route('/management')
@role_required('editor')
def management_page():
    return render_template('management.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if models.login_user(form.uid.data, form.password.data):
                u = models.User.query.filter_by(uid=form.uid.data).first()

                flask_login.login_user(u)
                return redirect('/')
            else:
                flash("Неверное имя пользователя или пароль")
        else:
            app.logger.debug("Invalid user login input: {}".format(get_form_errors(form)))
            flash_errors(form)
    return render_template('login.html', form=form, active_page="login")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route('/directive')
@role_required('editor')
def directive_page():
    return render_template('directive.html', cur_year=2018)


@app.route('/page/<name>')
def dynamic_page(name):
    page = models.Page.query.filter_by(name=name).first_or_404()
    return render_template('page.html', page=page)


@app.route('/page/<name>/edit', methods=('GET', 'POST'))
@role_required('editor')
def edit_dynamic_page(name):
    page = models.Page.query.filter_by(name=name).first_or_404()
    edit_form = forms.PageForm()
    if request.method == 'POST':
        if edit_form.validate_on_submit():
            app.logger.debug("Page with name %s is being edited", name)
            edit_form.populate_obj(page)
            page.last_edit = datetime.now()
            db.session.commit()
            if edit_form.make_advert.data:
                app.logger.debug("Making advert for changes on page %s", name)
                advert = models.Post()
                advert.advert_for = page
                advert.title = edit_form.advert_text.data
                db.session.add(advert)
                db.session.commit()
            return redirect('/page/{}'.format(page.name))
        else:
            app.logger.debug("Invalid PageForm input: {}".format(get_form_errors(edit_form)))
            flash_errors(edit_form)
    # Passing page data to form fields for editing
    edit_form.title_ru.data = page.title_ru
    # edit_form.title_en.data = page.title_en
    edit_form.text_ru.data = page.text_ru
    # edit_form.text_en.data = page.text_en
    return render_template("edit_page.html", edit_form=edit_form, page=page, add_file_form=forms.FileForm(),
                           edit_file_form=forms.FileEditForm(), remove_file_form=forms.FileRemoveForm())


@app.route('/page/<name>/archive')
@role_required('editor')
def archive_dynamic_page(name):
    page = models.Page.query.filter_by(name=name).first_or_404()
    if page.is_archive:
        abort(400)
    now = datetime.now()
    new_name = "{}{}".format(name, now.strftime("%Y%m%d"))
    # generating archive page unique name
    new_name_appendix = ""
    iteration = 1
    while True:
        if models.Page.query.filter_by(name=new_name + new_name_appendix).first() is None:
            break
        new_name_appendix = str(iteration)
        iteration += 1
    new_name += new_name_appendix
    # moving existing page and creating new page
    page.name = new_name
    new_page = models.Page()
    new_page.name = name
    new_page.content_as_given(page)
    db.session.add(new_page)
    db.session.commit()
    page.archivate(new_page)
    # TODO: расширить, когда будет i18n
    page.title_ru += " (Архив от {}{}{})".format(now.strftime("%d.%m.%Y"),
                                                 "/" if new_name_appendix else "",
                                                 new_name_appendix)  # FIXME: а если превысит лимит?
    db.session.commit()

    return redirect("/page/{}".format(name))


@app.route('/fm/list')
def list_files():
    files = [f.serialize() for f in models.File.query.all()]
    return jsonify(files)


@app.route('/fm/list/<target>/<tid>')
def list_target_files(target, tid):
    if target == 'post':
        files = [f.serialize() for f in models.File.query.filter_by(post_id=tid).all()]
    elif target == 'page':
        files = [f.serialize() for f in models.File.query.filter_by(page_id=tid).all()]
    else:
        app.logger.warning("Unknown file manager target: %s", target)
        files = []
    return jsonify(files)


@app.route('/fm/file/<fid>')
def file_info(fid):
    file = models.File.query.get(fid)
    if file is not None:
        return jsonify(file.serialize())
    else:
        return jsonify({"result": "not found"})


@app.route('/fm/add', methods=['POST'])
@role_required('editor')
def add_file():
    result = "invalid"
    form = forms.FileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            app.logger.debug("File is being added")
            mfile = models.File()
            form.page_id.data = None if not form.page_id.data else form.page_id.data
            form.post_id.data = None if not form.post_id.data else form.post_id.data
            form.populate_obj(mfile)
            mfile.file_name = ""
            mfile.file_size = 0
            db.session.add(mfile)
            db.session.commit()
            file = form.file.data
            try:
                filename = secure_filename("f_{}_{}".format(mfile.id, file.filename))
                way = os.path.join(mfile.uploading_directory, filename)
                os.makedirs(mfile.uploading_directory, exist_ok=True)
                file.save(way)
                size = os.stat(way).st_size
                mfile.file_name = filename
                mfile.file_size = size
                db.session.commit()
                result = "success"
            except Exception as e:
                app.logger.error('Error occurred while file adding', e)
                result = "failure"
        else:
            app.logger.debug("Invalid FileForm input: {}".format(get_form_errors(form)))

    return jsonify({"result": result})


@app.route('/fm/edit', methods=['POST'])
@role_required('editor')
def edit_file():
    result = "invalid"
    form = forms.FileEditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            app.logger.debug("File is being edited")
            mfile = models.File.query.get(form.file_id.data)
            if mfile is not None:
                form.populate_obj(mfile)
                db.session.commit()
                result = "success"
            else:
                result = "not found"
        else:
            app.logger.debug("Invalid FileForm input: {}".format(get_form_errors(form)))

    return jsonify({"result": result})


@app.route('/fm/remove', methods=['POST'])
@role_required('editor')
def remove_file():
    result = "invalid"
    form = forms.FileRemoveForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            app.logger.debug("File is being deleted")
            mfile = models.File.query.get(form.file_id.data)
            if mfile is not None:
                result = "success" if utils.remove_file(mfile) else "failure"
            else:
                result = "not found"
        else:
            app.logger.debug("Invalid FileRemoveForm input: {}".format(get_form_errors(form)))

    return jsonify({"result": result})

@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Доступ ограничен'  # TODO: change?


@babel.localeselector
def get_locale():
    loc = request.cookies.get("App-Language")
    if loc not in app.config["LANGUAGES"].keys():
        loc = request.accept_languages.best_match(app.config["LANGUAGES"].keys())
    loc = 'ru'  # remove when translations will be allowed
    g.locale = loc
    return loc


@app.route("/locale/set/<locale>")
def set_lang_cookie(locale):
    response = make_response(redirect('/'))
    if locale in app.config["LANGUAGES"].keys():
        response.set_cookie('App-Language', value=locale)
        g.locale = locale
    return response


@app.before_request
def prepare():
    g.locale = get_locale()  # FIXME: make something to not calculate it every time

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'),404
