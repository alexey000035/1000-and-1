import os

from imit import app, db
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPException, LDAPBindError
import flask_login
from datetime import datetime
from bs4 import BeautifulSoup
from imit.utils import first
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

ldap_server = Server(app.config['LDAP_SERVER'], port=app.config['LDAP_PORT'],
                     use_ssl=app.config['LDAP_USE_SSL'], get_info=ALL)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, index=True, nullable=False)
    description = db.Column(db.String(100))

    def __init__(self, title="", descr=None):
        self.title = title
        self.description = descr

    def __str__(self):
        return self.title


roles = db.Table('roles',
                 db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                 )


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password = db.Column(db.String(100))
    email = db.Column(db.String(50))
    roles = db.relationship('Role', secondary=roles)
    full_name = db.Column(db.String(50))
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    initials = db.Column(db.String(5))
    _is_authenticated = True

    def __init__(self, uid="", email=None, full_name=None,
                 first_name=None, second_name=None, initials=None,
                 uroles=None):
        if uroles is None:
            uroles = []
        self.uid = uid
        self.email = email
        self._is_authenticated = True
        self.roles = uroles
        self.full_name = full_name
        self.first_name = first_name
        self.second_name = second_name
        self.initials = initials

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def has_role(self, role):
        return role in [r.title for r in self.roles]
      
class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime())
    description = db.Column(db.Text())
    
    def __init__(self, date = None):
        if date is None:
            self.date_created = datetime.now()

class DraftAds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    
    def toAds(self):
        advert = Ads()
        advert.description = self.description
        return advert
      
class Agents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_empl = db.Column(db.Integer, db.ForeignKey('employers.id'))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    

class Employers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    logo = db.Column(db.String(150))
    link = db.Column(db.String(100))
    promo_link = db.Column(db.String(500))
    date = db.Column(db.DateTime())
    desc_company = db.Column(db.String(500))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    practice = db.Column(db.String(100))
    
    @property
    def has_cover_image(self):
        return self.logo is not None


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text())
    name = db.Column(db.Text())
    father_id = db.Column(db.Integer)
    size = db.Column(db.Integer)
    number = db.Column(db.Integer)

class Draft_post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    full_text = db.Column(db.Text())
    cover_image = db.Column(db.Boolean)
    
    @property
    def short_text(self):
        # fix: Если нет тегов => BeautifulSoup-> None
        # но функция str преобразовывала None -> "None"
        html = ""
        if self.full_text:
            html = BeautifulSoup(self.full_text, 'html.parser').p
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser').div
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser')
        if html:
            if str(html).replace(" ", "").replace(" ", "") == "<p></p>":
                html = ""

        return html  # self.full_text
    def toPost(self):
        post = Post()

        post.title = self.title
        post.full_text = self.full_text
        post.cover_image = self.cover_image
        post.is_danger = False
        return post

class Sug_post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    full_text = db.Column(db.Text())
    cover_image = db.Column(db.Text())
    date_created = db.Column(db.DateTime())

    def __init__(self, date=None):
        if date is None:
            self.date_created = datetime.now()  # TODO: check for timezone

    @property
    def short_text(self):
        # fix: Если нет тегов => BeautifulSoup-> None
        # но функция str преобразовывала None -> "None"
        html = ""
        if self.full_text:
            html = BeautifulSoup(self.full_text, 'html.parser').p
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser').div
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser')
        if html:
            if str(html).replace(" ", "").replace(" ", "") == "<p></p>":
                html = ""

        return html  # self.full_text
    
    def toPost(self):
        post = Post()

        post.title = self.title
        post.full_text = self.full_text
        post.cover_image = self.cover_image
        post.is_danger = False
        return post
    
    @property
    def has_cover_image(self):
        return self.cover_image is not None

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    type_post = db.Column(db.String(256))
    id_post = db.Column(db.Integer)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    full_text = db.Column(db.Text())
    date_created = db.Column(db.DateTime())
    cover_image = db.Column(db.Boolean)
    is_advert = db.Column(db.Boolean)
    is_danger = db.Column(db.Boolean)
    advert_for_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    advert_for = db.relationship('Page', backref=db.backref('adverts', lazy='dynamic'))
    
    def __init__(self, date=None):
        if date is None:
            self.date_created = datetime.now()  # TODO: check for timezone

    @property
    def is_advert(self):
        return self.advert_for is not None

    @property
    def is_dan(self):
        return self.is_danger


    @property
    def short_text(self):
        # fix: Если нет тегов => BeautifulSoup-> None
        # но функция str преобразовывала None -> "None"
        html = ""
        if self.full_text:
            html = BeautifulSoup(self.full_text, 'html.parser').p
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser').div
            if not html:
                html = BeautifulSoup(self.full_text, 'html.parser')
        if html:
            if str(html).replace(" ", "").replace(" ","") == "<p></p>":
                html = ""

        return html#self.full_text


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    file_size = db.Column(db.Integer)
    file_name = db.Column(db.String(512), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('files', lazy='dynamic'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    page = db.relationship('Page', backref=db.backref('files', lazy='dynamic'))
    uploaded = db.Column(db.DateTime())

    def __init__(self, file_name=None, description=None):
        self.file_name = file_name
        self.description = description
        self.uploaded = datetime.now()

    @property
    def has_description(self):
        return self.description is not None

    @property
    def human_file_size(self):
        if self.file_size is None:
            return ''
        if self.file_size < 1024:
            return str(self.file_size) + ' Б'
        if self.file_size / 1024 < 1024:
            return str(int(self.file_size / 1024)) + ' Кб'
        if self.file_size / 1024 / 1024 < 1024:
            return str(int(self.file_size / 1024 / 1024)) + ' Мб'
        return str(int(self.file_size / 1024 / 1024 / 1024)) + ' Гб'

    @property
    def downloading_path(self):
        subdir = str(self.uploaded.year) + "/" if self.uploaded else ""
        return "/files/" + subdir + self.file_name

    @property
    def uploading_directory(self):
        subdir = str(self.uploaded.year) if self.uploaded else ""
        return os.path.join(app.config['FILE_UPLOAD_PATH'], subdir)

    @property
    def inner_file_path(self):
        return os.path.join(self.uploading_directory, self.file_name)

    def serialize(self):
        return {"id": self.id, "description": self.description, "file_size": self.human_file_size,
                "file_name": self.file_name, "uploaded": self.uploaded.strftime("%Y.%m.%d") if self.uploaded else None,
                "downloading_path": self.downloading_path}


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)
    title_ru = db.Column(db.String(256))
    title_en = db.Column(db.String(256))
    text_ru = db.Column(db.UnicodeText(4294967295))
    text_en = db.Column(db.UnicodeText(4294967295))
    last_edit = db.Column(db.DateTime())

    is_archive = db.Column(db.Boolean)
    archive_of_page = db.Column(db.Integer)
    archived = db.Column(db.DateTime())

    def __init__(self):
        self.last_edit = datetime.now()

    def content_as_given(self, given):
        self.title_en = given.title_en
        self.title_ru = given.title_ru
        self.text_ru = given.text_ru
        self.text_en = given.text_en

    @property
    def title(self):
        t = getattr(self, "title_" + g.locale)
        return t if t else self.title_ru

    @property
    def text(self):
        t = getattr(self, "text_" + g.locale)
        return t if t else self.text_ru

    @property
    def archives(self):
        return Page.query.filter_by(archive_of_page=self.id)

    def archivate(self, archive_of):
        self.is_archive = True
        self.archived = datetime.now()
        self.archive_of_page = archive_of.id
        for arch in self.archives:
            arch.archive_of_page = archive_of.id


def get_ldap_user_data(uid):
    app.logger.debug("Trying to get LDAP data for user {}".format(uid))
    result = None
    if uid is None:
        return result
    try:
        c = Connection(ldap_server)
        c.bind()
        c.search(search_base="OU=people,DC=cs,DC=karelia,DC=ru",
                 search_filter="(uid=" + uid + ")", attributes=ALL_ATTRIBUTES)
        if len(c.response) > 0:
            result = c.response[0]
        else:
            app.logger.debug("User with uid {} not found in LDAP".format(uid))
        c.unbind()
    except LDAPException as e:
        app.logger.error("LDAP error: %s", e)
    return None if result is None else result['attributes']


def create_user_if_absent(uid):
    if User.query.filter_by(uid=uid).first() is not None:
        return None
    data = get_ldap_user_data(uid)
    if data is None:
        return False
    app.logger.info("Initializing user with uid %s", uid)
    try:
        user = User(uid=uid, email=first(data.get('mail')), full_name=first(data.get('cn')),
                    first_name=first(data.get('givenName')),
                    second_name=first(data.get('sn')), initials=first(data.get('initials')))
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        app.logger.error("Failed during user initialization: %s", e)
        return False
    return True


def login_user(uid, password):
    result = True
    if uid is None or password is None:
        app.logger.debug("Invalid input: None is not allowed")
        return result
    create_user_if_absent(uid)  # if user was not logged before
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        app.logger.debug("No such user {}".format(uid))
        return result
    try:
        c = Connection(ldap_server)
        c.bind()
        c.search(search_base="OU=people, DC=cs, DC=karelia, DC=ru",
                 search_filter="(uid={})".format(uid), attributes=[])
        if len(c.response) > 0:
            try:
                if c.rebind(user=c.response[0]['dn'], password=password):
                    app.logger.debug("User {} succeed to authenticate through LDAP".format(uid))
                    result = True
                else:
                    app.logger.debug("User {} failed to authenticate through LDAP".format(uid))
            except LDAPBindError as e:
                app.logger.error('Error in LDAP rebind: %s', e)
        c.unbind()
    except LDAPException as e:
        app.logger.error("LDAP error: %s", e)

    if not result and user.password is not None:
        result = check_password_hash(user.password, password)
    return result


@app.login_manager.user_loader
def get_user(uid):
    if uid is None:
        return None
    return User.query.get(uid)


@app.login_manager.request_loader
def request_user_loader(request):
    uid = request.form.get('uid')
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return None
    user.is_authenticated = login_user(uid, request.form.get('password'))
    return user
