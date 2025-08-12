from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PDF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    comments = db.relationship('Comment', backref='pdf', cascade="all, delete-orphan", lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdf.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pdfs = PDF.query.all()
    return render_template('index.html', pdfs=pdfs)

@app.route('/add', methods=['GET', 'POST'])
def add_pdf():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        comment_text = request.form.get('comment', '')
        pdf = PDF(title=title, url=url)
        db.session.add(pdf)
        db.session.commit()
        if comment_text:
            comment = Comment(pdf_id=pdf.id, text=comment_text)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pdf.html')

@app.route('/pdf/<int:pdf_id>', methods=['GET', 'POST'])
def pdf_detail(pdf_id):
    pdf = PDF.query.get_or_404(pdf_id)
    if request.method == 'POST':
        text = request.form['text']
        db.session.add(Comment(pdf_id=pdf_id, text=text))
        db.session.commit()
        return redirect(url_for('pdf_detail', pdf_id=pdf_id))
    comments = Comment.query.filter_by(pdf_id=pdf_id).order_by(Comment.timestamp.desc()).all()
    return render_template('pdf_detail.html', pdf=pdf, comments=comments)


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    """Remove a comment and redirect back to its PDF detail page."""
    comment = Comment.query.get_or_404(comment_id)
    pdf_id = comment.pdf_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('pdf_detail', pdf_id=pdf_id))

if __name__ == '__main__':
    app.run(debug=True)
