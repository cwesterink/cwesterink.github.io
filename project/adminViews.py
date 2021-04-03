from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response

from flask_admin import Admin, BaseView , AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from flask_login import LoginManager, current_user,login_user, logout_user, login_required

from .models import User
from . import db



class MyIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated is False:
            return False
        usr = User.query.filter_by(id=current_user.get_id()).first()

        if usr.role.access_Admin:
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print(name)
        return redirect(url_for('main_bp.unauthorized'))


class MainView(ModelView):
    can_create = False


    def is_accessible(self):
        if current_user.is_authenticated is False:
            return False
        usr = User.query.filter_by(id=current_user.get_id()).first()

        if usr.role.access_Admin:
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access

        return redirect(url_for('main_bp.unauthorized'))


class UserView(MainView):
    form_excluded_columns = ['password_hash', 'image']
    column_exclude_list = ['password_hash', "image",]
    column_list = ['role',"username","gender","bio"]
    form_choices = {
        'status': [('admin', 'Admin'), ('member', 'Member')],

        'gender': [('male', 'male'), ('female', 'female')]
    }



class RoleView(MainView):
    can_create = True
    form_excluded_columns = ['Users']
    column_list = ['id', "name", "access_Admin", "chat_Cmds"]



