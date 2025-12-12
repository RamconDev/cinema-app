from flask import Blueprint
from app.cinema import cinema_bp as cinema

from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from string import ascii_uppercase

from app import db
from app.cinema.forms import RegisterGenreForm, RegisterMovieForm, RegisterAuditoriumForm
from app.models.cinema_genre import Genre
from app.models.cinema_movie import Movie
from app.models.cinema_movie_genre import MovieGenre
from app.models.cinema_auditorium import Auditorium
from app.models.cinema_seat import Seat


@cinema.route('/')
def index():
    return render_template('index.html')
## Genre
#Create
@cinema.route('/movie/genre/create', methods=['GET', 'POST'])
def create_genre():
    form = RegisterGenreForm()

    if form.validate_on_submit():
        new_genre = Genre(
            name = form.name.data,
            description = form.description.data
        )

        try:
            db.session.add(new_genre)
            db.session.commit()
            flash("Genre Created", "success")
        except:
            db.session.rollback()
            flash("Error")
        return redirect( url_for('cinema.view_genres') )

    return render_template('cinema_genre_create.html', form=form)

# Read
@cinema.route("/movie/genre")
def view_genres():
    genres = db.session.execute(
            db.select(Genre).order_by(Genre.id.asc())
    ).scalars().all()

    return render_template("cinema_genre_list.html", list=genres)

# Update
@cinema.route("/movie/genre/<int:genre_id>", methods=['GET', 'POST'])
def update_genre(genre_id):
    genre = db.session.get(Genre, genre_id)
    if not genre:
        flash("Genre doesn't exist", "")
        return redirect( url_for('cinema.view_genres') )
    
    form = RegisterGenreForm(
        name = genre.name,
        description = genre.description
    )

    form.submit.label.text = 'Update'

    if form.validate_on_submit():
        genre.name = form.name.data
        genre.description = form.description.data

        try:
            db.session.commit()
            flash("Updated genre", "success")
        except:
            db.session.rollback()
            flash("The genre could not be updated due to integrity restrictions.", "error")
        return redirect( url_for("cinema.view_genres") )
    
    elif request.method == 'GET':
        form.name.data = genre.name
        form.description.data = genre.description

    return render_template("cinema_genre_create.html", form=form)

# Delete
@cinema.route("/movie/genre/<int:genre_id>/delete")
def delete_genre(genre_id):
    genre = db.session.get(Genre, genre_id)
    if not genre:
        flash("Role doesn't exist", "alert")
        return redirect( url_for('cinema.view_genres') )
    
    # if Movie.query.filter_by(genre_id=genre_id).count() > 0:
    #     flash("The genre in use cannot be deleted.")
    # else:
    try:
        db.session.delete(genre)
        db.session.commit()
        flash("Deleted genre", "success")
    except:
        db.session.rollback()
        flash("The role cannot be deleted due to integrity constraints.")
    #
    return redirect( url_for("cinema.view_genres") )

## Movie
# Create
@cinema.route("/movie/create", methods=['GET', 'POST'])
def create_movie():
    form = RegisterMovieForm()

    form.options.choices = [(g.id, g.name) for g in Genre.query.all()]

    if form.validate_on_submit():
        selected_genres = form.options.data

        new_movie = Movie(
            title = form.title.data,
            description = form.description.data,
            release_year = int(form.release_year.data),
            duration_minutes = form.duration_minutes.data,
            poster_url = form.poster_url.data
        )

        new_movie.movie_genres = [MovieGenre(genre_id=genre) for genre in selected_genres]

        try:
            db.session.add(new_movie)
            db.session.commit()
            flash("Movie Created", "success")
        except IntegrityError:
            db.session.rollback()
            flash('The movie could not be created: it already exists or there is an integrity conflict.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Unexpected error: {str(e)}', 'error')
        return redirect( url_for("cinema.view_movies") )

    return render_template("cinema_movie_create.html", form=form)

# Read
@cinema.route("/movie/list")
def view_movies():
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.id.desc())
    ).scalars().all()
    return render_template("cinema_movie_list.html", list=movies)

# Update
@cinema.route("/movie/<int:movie_id>", methods=['GET', 'POST'])
def update_movie(movie_id):

    movie = db.session.get(Movie, movie_id)
    if not movie:
        flash("Movie doesn't exist", "")
        return redirect( url_for('cinema.view_movies') )
    
    form = RegisterMovieForm(
        title = movie.title,
        description = movie.description,
        release_year = movie.release_year,
        duration_minutes = movie.duration_minutes,
        poster_url = movie.poster_url,
    )

    form.options.choices = [(g.id, g.name) for g in Genre.query.all()]
    form.submit.label.text = 'Update'

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        selected_genres = form.options.data

        movie.movie_genres = [MovieGenre(genre_id=genre) for genre in selected_genres]

        try:
            db.session.commit()
            flash("Updated movie", "success")
        except IntegrityError:
            db.session.rollback()
            flash('The movie could not be created: it already exists or there is an integrity conflict.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Unexpected error: {str(e)}', 'error')
        return redirect( url_for("cinema.view_movies") )
    
    elif request.method == 'GET':
        form.title.data = movie.title
        form.description.data = movie.description

        form.options.data = [mg.genre_id for mg in movie.movie_genres]

    return render_template("cinema_movie_create.html", form=form)

# Delete
@cinema.route("/movie/<int:movie_id>/delete")
def delete_movie(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        flash("Role doesn't exist", "alert")
        return redirect( url_for('cinema.view_movies') )
    
    # if Movie.query.filter_by(movie_id=movie_id).count() > 0:
    #     flash("The movie in use cannot be deleted.")
    # else:
    try:
        db.session.delete(movie)
        db.session.commit()
        flash("Deleted movie", "success")
    except:
        db.session.rollback()
        flash("The role cannot be deleted due to integrity constraints.")
    # 
    return redirect( url_for("cinema.view_movies") )

## Auditorium
# Create
@cinema.route("/cinema/auditorium/create", methods=['GET', 'POST'])
def create_auditorium():
    form = RegisterAuditoriumForm()

    if form.validate_on_submit():

        total_seats_calculated = form.rows.data * form.seats_per_row.data

        new_auditorium = Auditorium(
            name = form.name.data,
            total_seats = total_seats_calculated
        )
        try:
            db.session.add(new_auditorium)
            db.session.commit()

            seats_to_add = []

            rows_letters = ascii_uppercase[:form.rows.data]

            for row_letter in rows_letters:
                for seat_number_int in range(1, form.seats_per_row.data + 1):
                    # Genera el nombre del asiento (Ej: A1, B10)
                    seat_name = f"{row_letter}{seat_number_int}"
                    new_seat = Seat(
                        # Usamos la relación para vincular, aunque podemos usar el ID después
                        seat_number=seat_name,
                        auditorium_id=new_auditorium.id # SQLAlchemy lo adjunta automáticamente
                    )
                    seats_to_add.append(new_seat)
            
            db.session.add_all(seats_to_add)

            db.session.commit()
            flash("Added Auditorium", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Error: Ya existe", "alert")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la sala y asientos: {e}", "alert")

        return redirect( url_for("cinema.view_auditoriums") )

    return render_template("cinema_auditorium_create.html", form=form, auditorium=None, seats=[])

# Read
@cinema.route("/cinema/auditorium/list")
def view_auditoriums():
    auditorium_list = db.session.execute(
        db.select(Auditorium).order_by(Auditorium.name.asc())
    ).scalars().all()

    return render_template("cinema_auditorium_list.html", list=auditorium_list)

# Update
@cinema.route("/cinema/auditorium/<int:auditorium_id>", methods=['GET', 'POST'])
def update_auditorium(auditorium_id):
    auditorium = db.session.execute(
        db.select(Auditorium)
        .where(Auditorium.id == auditorium_id)
        .options(selectinload(Auditorium.seats)) # <-- CARGA EFICIENTE DE ASIENTOS
    ).scalar_one_or_none()

    if not auditorium:
        flash("Auditorium doesn't exist.", "alert")
        redirect( url_for("cinema.view_auditoriums") )

    form = RegisterAuditoriumForm(obj=auditorium)
    form.submit.label.text = 'Update'

    if form.validate_on_submit():
        pass

    seats_list_sorted = sorted(auditorium.seats, key=lambda s: s.id)

    seats_by_row = {}
    for seat in seats_list_sorted:
        row_letter = seat.seat_number[0]
        if row_letter not in seats_by_row:
            seats_by_row[row_letter] = []
        seats_by_row[row_letter].append(seat)

    return render_template("cinema_auditorium_edit.html", form=form, auditorium=auditorium, seats=seats_by_row)

# Delete
@cinema.route("/cinema/auditorium/<int:auditorium_id>/delete", methods=['GET'])
def delete_auditorium(auditorium_id):
    auditorium = db.session.get(Auditorium, auditorium_id)
    if not auditorium:
        flash("Auditorium doesn't exist", "alert")
        return redirect( url_for('cinema.view_auditoriums') )
    try:
        db.session.delete(auditorium)
        db.session.commit()
        flash("Deleted auditorium", "success")
    except:
        db.session.rollback()
        flash("The auditorium cannot be deleted due to integrity constraints.")
    #
    return redirect( url_for("cinema.view_auditoriums") )