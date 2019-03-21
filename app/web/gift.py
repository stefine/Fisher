from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.models.base import db
from app.models.gift import Gift
from app.viewmodel.my_gift import GiftViewModel
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts = Gift.get_user_gift(uid)
    isbn_list = [gift.isbn for gift in gifts]
    wish_count = Gift.wish_count(isbn_list)
    gift_model = GiftViewModel(gifts=gifts, wish_count=wish_count)
    return render_template('my_gifts.html', gifts=gift_model.assamble())


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        gift = Gift()
        gift.isbn = isbn
        gift.uid = current_user.id
        current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        with db.auto_commit():
            db.session.add(gift)
    else:
        flash("这本书已经添加进你的心愿清单或者赠送清单, 请勿重新添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



