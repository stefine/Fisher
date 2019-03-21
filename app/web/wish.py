from flask import url_for, redirect, flash, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from app.viewmodel.my_wish import WishViewModel
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes = Wish.get_user_wish(uid)
    isbn_list = [wish.isbn for wish in wishes]
    wish_count = Wish.wish_count(isbn_list)
    wish_model = WishViewModel(wishes, wish_count)
    return render_template('my_wish.html', wishes=wish_model.assamble())


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        wish = Wish()
        wish.isbn = isbn
        wish.uid = current_user.id
        with db.auto_commit():
            db.session.add(wish)
    else:
        flash("这本书已经添加进你的心愿清单或者赠送清单, 请勿重新添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
