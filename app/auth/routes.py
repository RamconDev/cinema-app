from flask import Blueprint
from app.auth import auth_bp as auth

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from wtforms.validators import DataRequired


from app import db
from app.auth.forms import RegisterNewUserForm, RegisterRoleForm
from app.models.auth_user import User
from app.models.auth_role import Role

## ROLES
# Create
@auth.route('/user/role/create', methods=['GET', 'POST'])
def register_role():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('cinema.index'))
    
    form = RegisterRoleForm()

    if form.validate_on_submit():
        new_role = Role(
            name = form.name.data,
            description = form.description.data
        )
        db.session.add(new_role)
        db.session.commit()
        flash('Role Created', 'alert')
        return redirect( url_for('cinema.index') )
    return render_template('auth_role_create.html', form=form)

# Read
@auth.route('/user/role/list')
def view_roles():
    roles = db.session.execute(
        db.select(Role).order_by(Role.id.asc())
    ).scalars().all()

    return render_template('auth_role_list.html', roles=roles)

# Update
@auth.route('/user/role/<int:role_id>', methods=['GET', 'POST'])
def update_role(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        flash("Role doesn't exist", "")
        return redirect( url_for('view_roles') )
    
    form = RegisterRoleForm(
        name = role.name,
        description = role.description
    )

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data

        db.session.commit()
        flash("Updated role", "success")
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
        flash("Role doesn't exist", "")
        return redirect( url_for('view_roles') )
    
    db.session.delete(role)
    db.session.commit()
    flash("Deleted role", "")
    return redirect( url_for('auth.view_roles') )

## USERS
# CREATE
@auth.route('/user/create', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('cinema.index'))
    
    form = RegisterNewUserForm()

    roles = Role.query.all()
    form.password.validators = [DataRequired()]
    form.role.choices = [('2', '-- Default --')] + [(r.id, r.name) for r in roles]
    
    if form.validate_on_submit():
        new_user = User.create_user(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data,
            role_id = form.role.data
        )

        db.session.add(new_user)
        db.session.commit()
        flash('register successful')
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
    form.role.choices = [(user.role_id, f'-- { user.roles.name } --')] + [(role.id, role.name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.role_id = form.role.data

        if form.password.data:
            user.password_hash = form.password.data

        db.session.commit()
        flash("User updated successfully", "")
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
    
    db.session.delete(user)
    db.session.commit()
    flash("Deleted user", "")
    return redirect( url_for('auth.view_users') )
#

@auth.route('/login')
def login():
    pass

@auth.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('cinema.index') )