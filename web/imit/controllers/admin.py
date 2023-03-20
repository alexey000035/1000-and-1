from flask_admin.menu import MenuLink
from imit import app, models, forms, db, admin
from imit.utils import flash_errors, get_form_errors
from flask import request, url_for, redirect, flash
import flask_login
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView


# Overriding admin authorization for model views
class ImitModelView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


# Overriding admin authorization for other views    
class ImitBaseView(BaseView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class InitUserView(ImitBaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = forms.InitUserForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                is_created = models.create_user_if_absent(form.uid.data)
                if is_created is None:
                    flash("Ошибка при инициализации пользователя {}, "
                          "проверьте, может быть он уже инициализирован".format(form.uid.data))
                elif is_created:
                    flash("Пользователь {} успешно инициализирован".format(form.uid.data))
                else:
                    flash("Пользователь {} отсутствует на сервере аутентификации".format(form.uid.data))
            else:
                app.logger.debug("Invalid uid input: {}".format(get_form_errors(form)))
                flash_errors(form)
        return self.render('admin/init_user.html', form=form)


class CreateCustomUserView(ImitBaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = forms.CreateCustomUserForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user = models.User.query.get(form.uid.data)
                if user is None:
                    try:
                        nuser = models.User(uid=form.uid.data)
                        nuser.set_password(form.password.data)
                        db.session.add(nuser)
                        db.session.commit()
                        flash("Пользователь {} успешно создан".format(form.uid.data))
                    except Exception as e:
                        app.logger.error("Failed during user creation: %s", e)
                        flash("Ошибка при создании пользователя '{}': {}".format(form.uid.data, e))
                else:
                    flash("Пользователь с uid '{}' уже существует".format(form.uid.data))
            else:
                app.logger.debug("Invalid form input: {}".format(get_form_errors(form)))
                flash_errors(form)
        return self.render('admin/create_custom_user.html', form=form)


# Adding administrative interface
admin.add_link(MenuLink(name='Imit', category='', url='/'))
admin.add_view(ImitModelView(models.User, db.session))
admin.add_view(ImitModelView(models.Role, db.session))
admin.add_view(InitUserView(name='InitUser', endpoint='init_user'))
admin.add_view(CreateCustomUserView(name='CreatePwUser', endpoint='create_custom_user'))
admin.add_view(ImitModelView(models.Page, db.session))
admin.add_view(ImitModelView(models.File, db.session))
