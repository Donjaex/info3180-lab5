"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from .forms import MovieForm
from .models import Movie
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title       = form.title.data
        description = form.description.data
        poster_file = form.poster.data

        filename = secure_filename(poster_file.filename)

        # Save file to uploads folder
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        poster_file.save(os.path.join(upload_folder, filename))

        # Save to database
        movie = Movie(title=title, description=description, poster=filename)
        db.session.add(movie)
        db.session.commit()

        return jsonify({
            'message':     'Movie Successfully added',
            'title':       title,
            'poster':      filename,
            'description': description
        })

    return jsonify({'errors': form_errors(form)}), 400


@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = [
        {
            'id':          m.id,
            'title':       m.title,
            'description': m.description,
            'poster':      f'/api/v1/posters/{m.poster}'
        }
        for m in movies
    ]
    return jsonify({'movies': movie_list})


@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


###
# The functions below should be applicable to all Flask apps.
###

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404