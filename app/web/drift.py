from flask import flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.spider.yushu_book import Yushubook
from app.viewmodel.book import BookViewModel
from app.viewmodel.drift import DriftViewModel
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
def send_drift(gid):
    my_gift = Gift.query.get_or_404(gid)
    if my_gift.is_your_gift(current_user.id):
        flash("这本书就是你的，无法自我请求")
        return redirect(url_for('web.book_detail', isbn=my_gift.isbn))
    if not current_user.can_send_drift():
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, my_gift)
        return redirect(url_for('web.pending'))
    gifter = my_gift.user.summary
    return render_template('drift.html', gifter=gifter,
                           user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    view_model = DriftViewModel(drifts, current_user.id)
    views = view_model.collection()
    return render_template('pending.html', drifts=views)


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did).first_or_404()
        drift.pending = PendingStatus.redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


def save_drift(drift_form, my_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = my_gift.id
        drift.requester_id = current_user.id
        drift.recipient_name = current_user.nickname
        drift.gifter_nickname = my_gift.user.nickname
        drift.gifter_id = my_gift.user.id

        yushu_book = Yushubook()
        yushu_book.search_by_isbn(isbn=my_gift.isbn)
        book = BookViewModel.collection(data=yushu_book)['books'][0]

        drift.book_author = book['author']
        drift.book_img = book['image']
        drift.book_title = book['title']
        drift.pending = PendingStatus.waiting

        db.session.add(drift)
