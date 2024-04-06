from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Event %r>' % self.id


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/events')
def events():
    articles = Event.query.order_by(Event.date.desc()).all()
    return render_template("events.html", articles=articles)


@app.route('/events/<int:id>')
def event_detail(id):
    article = Event.query.get(id)
    return render_template("event_detail.html", article=article)


@app.route('/events/<int:id>/delete')
def event_delete(id):
    article = Event.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/events')
    except:
        return "При удалении произошла ошибка"


@app.route('/events/<int:id>/update', methods=['POST', 'GET'])
def event_update(id):
    article = Event.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']
        article.date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        try:
            db.session.commit()
            return redirect('/events')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("event_update.html", article=article)


@app.route('/')
@app.route('/main', methods=['POST', 'GET'])
def create_event():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        article = Event(title=title, date=date, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/main')
        except:
            return "При добавлении события произошла ошибка"
    else:
        return render_template("main.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)