from app.public import public_bp as public

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from app.public.forms import ReservationsSeatsForm

from app import db
from app.models.cinema_movie import Movie
from app.models.cinema_function import CinemaFunction
from app.models.public_reservation import Reservation
from app.models.public_reservation_seats import ReservationSeats

@public.route('/')
def index():
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.release_year.desc())
    ).scalars().all()

    return render_template("public_index.html", movies=movies)

@public.route('/movie/<int:movie_id>')
def info_movie(movie_id):
    movie = db.session.get(Movie, movie_id)

    if not movie:
        return redirect( url_for('public.index', movie_id=movie_id) )

    functions_movie = [fm for fm in movie.cinema_functions if fm.start_function >= datetime.now()]

    return render_template("public_movie_single.html", movie=movie, functions_movie=functions_movie)

@public.route("/movie/<int:movie_id>/function/<int:function_id>", methods=['GET', 'POST'])
def info_function(movie_id ,function_id):
    movie_function = db.session.get(CinemaFunction, function_id)

    if not movie_function:
        flash("Function doesn't exist.")
        return redirect( url_for('public.info_movie', movie_id=movie_id) )
    
    form = ReservationsSeatsForm()

    seats_list_sorted = sorted(movie_function.auditorium.seats, key=lambda s: s.id)
    
    form.seats.choices = [(s.id, s.seat_number) for s in seats_list_sorted]

    reservations = Reservation.query.all()

    res = db.session.get(CinemaFunction, function_id)

    seatss = []
    print (res)
    for re in res.reservations:
        for seat in re.reservation_seats:
            seatss.append(seat.seat_id)

    print(seatss)
    # seats_by_row = {}
    # for seat_id, seat_number in form.seats.choices:
    #     row_letter = seat_number[0]
    #     if row_letter not in seats_by_row:
    #         seats_by_row[row_letter] = []
    #     seats_by_row[row_letter].append((seat_id, seat_number))

    if form.validate_on_submit():
        user_id = current_user.id
        seats_selected = form.seats.data
        reservation = Reservation(
            user_id = user_id,
            function_id = movie_function.id,
            status = 'Reserved'
        )

        db.session.add(reservation)
        db.session.commit()

        for seat in seats_selected:
            new_seat = ReservationSeats(
                reservation_id = reservation.id,
                seat_id = seat
            )
            db.session.add(new_seat)

        try:
            db.session.commit()
            flash("Done Reservation", "success")

        except:
            db.session.rollback()
            flash("Error", "alert")

    return render_template("public_function_single.html", form=form, function=movie_function, reservations=reservations)