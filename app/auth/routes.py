from app.auth import auth_bp as auth

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from wtforms.validators import DataRequired, Optional
from sqlalchemy.exc import IntegrityError

from app import db
from app.auth.forms import RegisterNewUserForm, RegisterRoleForm, LoginUserForm
from app.models.auth_user import User
from app.models.auth_role import Role

## ROLES
# Create
@auth.route('/user/role/create', methods=['GET', 'POST'])
def register_role():
    # if current_user.is_authenticated:
    #     flash('You are already logged in.', 'info')
    #     return redirect(url_for('cinema.index'))
    
    form = RegisterRoleForm()

    if form.validate_on_submit():
        new_role = Role(
            name = form.name.data,
            description = form.description.data
        )
        try:
            db.session.add(new_role)
            db.session.commit()
            flash('Role Created', 'alert')
        except IntegrityError:
            db.session.rollback()
            flash('The role could not be created: it already exists or there is an integrity conflict.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Unexpected error: {str(e)}', 'error')
        return redirect( url_for('auth.view_roles') )
    return render_template('auth_role_create.html', form=form)

# Read
@auth.route('/user/role/list')
def view_roles():
    roles = db.session.execute(
        db.select(Role).order_by(Role.id.asc())
    ).scalars().all()

    return render_template("auth_role_list.html", roles=roles)

# Update
@auth.route('/user/role/<int:role_id>', methods=['GET', 'POST'])
def update_role(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        flash("Role doesn't exist", "")
        return redirect( url_for('auth.view_roles') )
    
    form = RegisterRoleForm(
        name = role.name,
        description = role.description
    )

    form.submit.label.text = 'Update'

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data

        try:
            db.session.commit()
            flash("Updated role", "success")
        except:
            db.session.rollback()
            flash("The role could not be updated due to integrity restrictions.", "error")
        return redirect( url_for('auth.view_roles') )
    
    elif request.method == 'GET':
        form.name.data = role.name
        form.description.data = role.description

    return render_template('auth_role_create.html', form=form)

# Delete
@auth.route('/user/role/<int:role_id>/delete', methods=['GET'])
def delete_role(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        flash("Role doesn't exist", "alert")
        return redirect( url_for('auth.view_roles') )
    
    if User.query.filter_by(role_id=role_id).count() > 0:
        flash("The role in use cannot be deleted.")
    else:
        try:
            db.session.delete(role)
            db.session.commit()
            flash("Deleted role", "")
        except:
            db.session.rollback()
            flash("The role cannot be deleted due to integrity constraints.")
    return redirect( url_for('auth.view_roles') )

## USERS
# CREATE
@auth.route('/user/create', methods=['GET', 'POST'])
def register_user():    
    form = RegisterNewUserForm()

    roles = Role.query.all()
    form.password.validators = [DataRequired()]
    form.role.choices = [(2, '-- Default --')] + [(r.id, r.name) for r in roles]
    
    if form.validate_on_submit():
        new_user = User.create_user(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data,
            role_id = form.role.data
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('register successful')
        except IntegrityError:
            db.session.rollback()
            flash("The user could not be created: it already exists or there is an integrity conflict.", "error")
        except Exception as e:
            db.session.rollback()
            flash("Unexpected error: {str(e)}", "error")
        return redirect( url_for('auth.view_users') )

    return render_template('auth_user_create.html', form=form)

# READ
@auth.route('/user/list')
def view_users():
    users = db.session.execute(
        db.select(User).order_by(User.id.desc())
    ).scalars().all()

    return render_template('auth_user_list.html', users=users)

# UPDATE
@auth.route('/user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User doesn't exists", "info")
        return redirect( url_for('auth.view_users') )

    form = RegisterNewUserForm(user=user)
    form.password.validators = []
    roles = Role.query.all()
    form.role.choices = [(0, "-- Select Role --")] + [(role.id, role.name) for role in roles]
    form.submit.label.text = 'Update'
    
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.role_id = form.role.data

        if form.password.data:
            user.password_hash = form.password.data

        try:
            db.session.commit()
            flash("User updated successfully", "")
        except:
            db.session.rollback()
            flash("The user could not be updated due to integrity restrictions.", "")
        return redirect( url_for('auth.view_users') )
    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.role.data = user.role_id

    return render_template('auth_user_create.html', form=form)


# DELETE
@auth.route('/user/<int:user_id>/delete')
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User doesn't exist", "")
        return redirect( url_for('view_users') )
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash("Deleted user", "")
    except:
        db.session.rollback()
        flash("The user cannot be deleted due to integrity constraints.", "")
    return redirect( url_for('auth.view_users') )
#

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()

    if current_user.is_authenticated:
        flash("You already have an active session.", "alert")

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter(
            User.email == form.email.data
        )).scalar_one_or_none()

        if not user or not user.check_password(form.password.data):
            flash("Datos invalidaos", "alert-danger")
            return redirect( url_for("auth.login") )
        
        login_user(user, form.stay_loggedin.data)

        next_page = request.args.get('next')

        flash(f"Welcome {user.name.capitalize()}", "alert-success")
        return redirect( next_page or url_for('cinema.index') )

    return render_template('auth_login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterNewUserForm()

    form.role.choices = [(2, 'User')]
    form.role.validators = [Optional()]

    if form.validate_on_submit():
        new_user = User.create_user(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data,
            role_id = 2
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('register successful')
        except IntegrityError:
            db.session.rollback()
            flash("The user could not be created: it already exists or there is an integrity conflict.", "error")
        except Exception as e:
            db.session.rollback()
            flash("Unexpected error: {str(e)}", "error")
        return redirect( url_for('auth.login') )

    return render_template('auth_register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('cinema.index') )