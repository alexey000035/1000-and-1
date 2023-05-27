from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, HiddenField, TextAreaField, validators, BooleanField, IntegerField
from wtforms.fields import DateField
from wtforms.fields.simple import MultipleFileField

class LoginForm(FlaskForm):
    uid = StringField("Имя пользователя",
                      [validators.InputRequired(message="Обязательно к заполнению"),
                       validators.Length(min=3, max=30)])
    password = PasswordField("Пароль",
                             [validators.InputRequired(message="Обязательно к заполнению"),
                              validators.Length(min=3, max=30)])

class AdsForm(FlaskForm):
    description = TextAreaField("Текст", [validators.InputRequired()])
    date = StringField("Date", [validators.Optional(),
                                validators.Regexp(r"^\d\d\.\d\d\.\d\d\d\d$")])
    #date = StringField("Date", [validators.Optional(), validators.Regexp(r"^\d\d\d\d.\d\d\.\d\d$")])

class DraftAdsForm(FlaskForm):
    description = TextAreaField("Текст", [validators.InputRequired()])
    

class NewsForm(FlaskForm):
    title = StringField("Заголовок",
                        [validators.InputRequired(),
                         validators.Length(min=3, max=256,
                                           message="Необходим текст не более 256 символов и не менее 3")])
    delete_cover_image = BooleanField("", default=False)
    full_cover_image = MultipleFileField("Титульное изображение",
                                 [validators.Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'],
                                                                     'Допустимы только файлы изображений!')])
    cropped_cover_image_data = \
        HiddenField("", [validators.Optional(),
                         validators.Regexp(r"^data:image\/png;base64,[A-Za-z0-9!$&',()*+;=\-._~:@\/?%\s]+$")])
    full_text = TextAreaField("Текст", [validators.InputRequired()])
    date = StringField("Дата", [validators.Optional(),
                                validators.Regexp(r"^\d\d\.\d\d\.\d\d\d\d$")])

class MenuForm(FlaskForm):
    link = StringField("Ссылка")
    name = StringField("Заголовок",
                        [validators.InputRequired(),
                         validators.Length(min=3, max=100,
                                           message="Необходим текст не более 100 символов и не менее 1")])
    size = IntegerField("Размер заголовка(h2 или h3)", [validators.InputRequired(),
                         validators.NumberRange(min=2, max=3,
                                           message="Необходимо число от 2 до 3")], default=2)
    father = StringField("К какому пункту меню относится ",default=None)
    number = IntegerField("Номер пункта меню")

class InitUserForm(FlaskForm):
    uid = StringField("Имя пользователя",
                      [validators.InputRequired(message="Обязательно к заполнению"),
                       validators.Length(min=3, max=30)])


class CreateCustomUserForm(FlaskForm):
    uid = StringField("Имя пользователя",
                      [validators.InputRequired(message="Обязательно к заполнению"),
                       validators.Length(min=3, max=30)])
    password = PasswordField("Пароль",
                             [validators.InputRequired(message="Обязательно к заполнению"),
                              validators.Length(min=6, max=30)])

class EmployerAgent(FlaskForm):
    name = StringField("Имя", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    surname = StringField("Фамилия", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    second_name = StringField("Отчество", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    email = StringField("Почта", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    phone = StringField("Телефон", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    telegram = StringField("Телеграм или другой мессенджер", [validators.InputRequired(), validators.Length(min=1, max=20, message="Необходим текст не более 20 символов и не менее 1")])
    id_empl = IntegerField("Ident company")

class EmployersForm(FlaskForm):
    name = StringField("Название компании", [validators.InputRequired(), validators.Length(min=1, max=100, message="Необходим текст не более 100 символов и не менее 1")])
    logo = StringField("Логотип")
    link = StringField("Сылка на страницу компании", [validators.InputRequired(), validators.Length(min=1, max=100, message="Необходим текст не более 100 символов и не менее 1")])
    promo_link = StringField("Ссылка на компанию", [validators.InputRequired(), validators.Length(min=1, max=100, message="Необходим текст не более 100 символов и не менее 1")])
    date = DateField('Дата вакансии', format='%Y-%m-%d')    
    desc_company =  TextAreaField("Описание компании", [validators.InputRequired()])
    email = StringField("Почта")
    phone = StringField("Телефон")
    practice = StringField("Прохождение практики")
    cropped_cover_image_data = \
        HiddenField("", [validators.Optional(),
                         validators.Regexp(r"^data:image\/png;base64,[A-Za-z0-9!$&',()*+;=\-._~:@\/?%\s]+$")])
    full_cover_image = FileField("Титульное изображение",
                                 [validators.Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'],
                                                                     'Допустимы только файлы изображений!')])
    delete_cover_image = BooleanField("", default=False)


class PageForm(FlaskForm):
    title_ru = StringField("Заголовок",
                           [validators.InputRequired(),
                            validators.Length(min=3, max=256,
                                              message="Необходим текст не более 256 символов и не менее 3")])
    text_ru = TextAreaField("Текст", default="")
    # title_en = StringField("Заголовок на английском",
    #                       [validators.InputRequired(),
    #                        validators.Length(min=3, max=256,
    #                                          message="Необходим текст не более 256 символов и не менее 3")])
    # text_en = TextAreaField("Текст на английском", default="")
    make_advert = BooleanField("Сделать объявление об изменении", [validators.Optional()])
    advert_text = StringField("Текст объявления",
                              [validators.Optional(),
                               validators.Length(min=0, max=256,
                                                 message="Необходим текст не более 256 символов")])


class FileForm(FlaskForm):
    file = FileField("Файл", [FileRequired()])
    description = StringField("Описание", [validators.InputRequired()])
    post_id = HiddenField("Новость", [validators.Optional()])
    page_id = HiddenField("Страница", [validators.Optional()])


class FileEditForm(FlaskForm):
    file_id = HiddenField("Идентификатор файла", [validators.InputRequired()])
    description = StringField("Описание", [validators.InputRequired()])


class FileRemoveForm(FlaskForm):
    file_id = HiddenField("Идентификатор файла", [validators.InputRequired()])

class FAQFileForm(FlaskForm):
    file = FileField("Файл", [FileRequired(), FileAllowed(['js','json', 'txt'], "Только файлы JSON допустимы.")])

