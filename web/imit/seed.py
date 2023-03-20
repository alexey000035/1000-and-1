from imit import app, db, models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os.path


# Initializing database structure if none
if not db.engine.dialect.has_table(db.engine, "role"):
    app.logger.info("Initializing database")
    db.create_all()
    db.session.commit()

# Adding data
role1 = models.Role("editor", "")
role2 = models.Role("admin", "")
user = models.User("test_user", uroles=[role1, role2])
user.set_password("qwerty")
post = models.Post()
post.title = "test"
post.full_text = "<p>test full text</p> <p>another test text</p>"
db.session.add(role1)
db.session.add(role2)
db.session.add(user)
db.session.add(post)
db.session.commit()

st_page = models.Page()
st_page.name = 'structure'
st_page.title_ru = "Структура института"
st_page.text_ru = """<div class="item">
        <div>
            <h3>Дирекция</h3>
            <p style="margin:0px 0px 0px 20px;"><b>Директор:</b> Светова Нина Юрьевна, кандидат наук, доцент</p>
            <p style="margin:0px 0px 0px 20px;"><b>Заместитель директора:</b> Бородин Александр Владимирович, </p>
            <p style="margin:0px 0px 0px 20px;"><b>Cпециалисты по работе со студентами:</b>
            <div style="margin-left:80px;">
        Панченко Татьяна Борисовна. <a href="mailto:pmik@petrsu.ru">pmik@petrsu.ru</a><br>
        Панченко Анастасия Сергеевна. <a href="mailto:mathemat@petrsu.ru">mathemat@petrsu.ru</a> <br>
        Саблина Алла Михайловна. <a href="mailto:kafedra_atv@petrsu.ru">kafedra_atv@petrsu.ru</a>
            </div>
            </p>
            <p style="margin:5px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 255 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-10-78</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> nsvetova@petrsu.ru</p>

            <h3><a href="https://petrsu.ru/structure/288/matanaliz">Кафедра математического анализа</a></h3>
            <p style="margin:-10px 0px 0px 20px;"><b>Заведующий кафедрой:</b> Старков Виктор Васильевич, доктор наук,
                профессор</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 242 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-10-76</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> vstar@petrsu.ru</p>
            <p style="margin:0px 0px 0px 20px;"><b>Сайт:</b> <a href="http://analysis.petrsu.ru/">http://analysis.petrsu.ru/</a>
            </p>

            <h3><a href="https://petrsu.ru/structure/289/kafedraprikladnojmat">Кафедра прикладной математики и
                кибернетики</a></h3>
            <p style="margin:-10px 0px 0px 20px;"><b>Заведующий кафедрой:</b> Воронин Анатолий Викторович, доктор наук,
                профессор</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 270 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-10-68</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> pmik@petrsu.ru</p>
            <p style="margin:0px 0px 0px 20px;"><b>Сайт:</b> <a href="http://pmik.petrsu.ru/">http://pmik.petrsu.ru/</a>
            </p>

            <h3><a href="https://petrsu.ru/structure/290/kafedrainformatikiim">Кафедра информатики и математического
                обеспечения</a></h3>
            <p style="margin:-10px 0px 0px 20px;"><b>Заведующий кафедрой:</b> Богоявленский Юрий Анатольевич, кандидат
                наук, доцент</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 215 и 217 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-10-84, (814-2)71-10-15</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> ybgv@cs.karelia.ru</p>
            <p style="margin:0px 0px 0px 20px;"><b>Сайт:</b> <a href="http://cs.petrsu.ru/">http://cs.petrsu.ru/</a></p>

            <h3><a href="https://petrsu.ru/structure/291/kafedrateoriiveroyat">Кафедра теории вероятностей и анализа
                данных</a></h3>
            <p style="margin:-10px 0px 0px 20px;"><b>Заведующий кафедрой:</b> Рогов Александр Александрович, доктор
                наук, профессор</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 268 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-96-21</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> kafedra_atv@psu.karelia.ru</p>
            <p style="margin:0px 0px 0px 20px;"><b>Сайт:</b> <a href="http://tvad.petrsu.ru/">http://tvad.petrsu.ru/</a>
            </p>

            <h3><a href="https://petrsu.ru/structure/363/kafedrageometriiitop">Кафедра геометрии и топологии</a></h3>
            <p style="margin:-10px 0px 0px 20px;"><b>Заведующий кафедрой:</b> Иванов Александр Владимирович, доктор
                наук, профессор</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 230 каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-96-19</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> ivanov@petrsu.ru</p>


            <h3><a href="https://petrsu.ru/structure/468/kafedrateoriiimetodi">Кафедра теории и методики обучения
                математике и информационно-коммуникационным технологиям в образовании</a></h3>
            <p style="margin:-10px 0px 0px 20px;">Филимонова Елена Валерьевна, кандидат наук, доцент</p>
            <p style="margin:0px 0px 0px 20px;"><b>Адрес:</b> Главный корпус (пр. Ленина, д. 33), 430Б каб.</p>
            <p style="margin:0px 0px 0px 20px;"><b>Телефон(ы):</b> (814-2) 71-10-80</p>
            <p style="margin:0px 0px 0px 20px;"><b>Email:</b> geometry@petrsu.ru, kafinf@petrsu.ru</p>

        </div>
        <div style="clear: left; height: 1em;"></div>
    </div>"""

mag_templates = models.Page()
mag_templates.name = 'mag_templates'
mag_templates.title_ru = "Образцы индивидуальных планов и ведомостей"
mag_templates.text_ru = """
    <div class="item">&nbsp;Уважаемые магистранты первого года обучения! Ниже приложены бланки документов для оформления индивидуальных планов обучения в магистратуре института математики и информационных технологий.</div>
        <div class="item"><a href="../../files/f_2_2016_Obrazets_ind_plana_magistranta_-_PFM_M.docx">2016 Образец инд. плана магистранта - ПФМ М</a></div>
        <div class="item"><a href="../../files/f_3_2016_Obrazets_ind_plana_magistranta_-_MMKN_PMiI.docx">2016 Образец инд. плана магистранта - ММКН ПМиИ</a></div>
        <div class="item"><a href="../../files/f_4_2016_Obrazets_ind_plana_magistranta_-_STS_PMiI.docx">2016 Образец инд. плана магистранта - СТС ПМиИ</a></div>
        <div class="item"><a href="../../files/f_5_2016_Obrazets_ind_plana_magistranta_-_UD_ISiT.docx">2016 Образец инд. плана магистранта - УД ИСиТ</a></div>
        <div class="item"><a href="../../files/f_6_2016_Obrazets_ind_plana_magistranta_-_R_ISiT.docx">2016 Образец инд. плана магистранта - Р ИСиТ</a></div>
        <div class="item"><a href="../../files/f_1_2016_Obrazets_blanka_zameny_distsipliny_v_ind_plane.docx">2016 Образец бланка замены дисциплины в инд. плане</a></div>
        <div class="item"><a href="../../files/f_7_2016_Vedomost_na_1_semestr_dlya_kazhdoy_magisterskoy_programmy.docx">2016 Ведомость на 1 семестр для каждой магистерской программы</a></div>
        <div class="item">&nbsp;</div>
    """
db.session.add(st_page)
db.session.add(mag_templates)
db.session.commit()
