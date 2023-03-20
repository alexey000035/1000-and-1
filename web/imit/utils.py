from imit import app, db
import flask_login
from functools import wraps
from flask import flash
import os
import requests as req
from datetime import datetime
import pytz


def role_required(role):
    def role_decorator(func):
        @wraps(func)
        @flask_login.login_required
        def decorated_view(*args, **kwargs):
            if not (flask_login.current_user.has_role(role) or flask_login.current_user.has_role('admin')):
                return app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view

    return role_decorator


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Ошибка в поле %s - %s" % (
                getattr(form, field).label.text,
                error
            ))


def get_form_errors(form):
    e = {}
    for field, errors in form.errors.items():
        for error in errors:
            e[getattr(form, field).label.text] = error
    return e


def first(lst):
    return lst[0] if lst else None


def remove_file(file):
    result = True
    try:
        os.remove(file.inner_file_path)
        db.session.delete(file)
        db.session.commit()
    except Exception as e:
        app.logger.error('Error occurred while file deletion: %s', e)
        result = False

    return result


def get_vk_wall_posts(owner_id="-46264391", count=10):
    try:
        api_result = req.get(
            "https://api.vk.com/method/wall.get?owner_id={}&count={}&photo_sizes=1&v=5.62&access_token={}".format(owner_id, count, app.config["VK_API_KEY"]))
        j = api_result.json()
    except req.exceptions.RequestException as e:
        app.logger.error("Failed during VK query: %s", e)
        j = {"response": {"items": []}}
    if j.get("error") is not None:
        app.logger.error("VK request failed: %s", j["error"]["error_msg"])
        j = {"response": {"items": []}}
    return j["response"]["items"]


def get_vk_wall_post(post_id, owner_id="-46264391"):
    try:
        api_result = req.get("https://api.vk.com/method/wall.getById?posts={}_{}&v=5.62&access_token={}".format(owner_id, post_id, app.config["VK_API_KEY"]))
        j = api_result.json()
    except req.exceptions.RequestException as e:
        app.logger.error("Failed during VK query: %s", e)
        j = None
    if j.get("error") is not None:
        app.logger.error("VK request failed: %s", j["error"]["error_msg"])
        j = None
    return None if j is None else first(j["response"])


def convert_vk_post(post):
    attachments = [{"title": d["doc"]["title"], "url": d["doc"]["url"]}
                   for d in post.get("attachments", []) if d["type"] == "doc"]
    text = "<p>{}</p>".format(post["text"]) if len(post["text"]) > 0 else ""
    reposts = post.get("copy_history", None)
    if reposts is not None:
        for repost in reposts:
            inner = convert_vk_post(repost)
            text += inner["text"]
            attachments += inner["docs"]
    return {"title": "-", "text": text, "id": post["id"], "origin": "vk",
            "docs": attachments, "date": datetime.fromtimestamp(post["date"], tz=pytz.timezone('Europe/Moscow'))}
