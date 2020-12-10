from flask import Blueprint, render_template, redirect, request, url_for, session, flash
math = Blueprint('math', __name__, static_folder='static', template_folder='templates')


from calculator import math


@math.route('/calculator', methods = ['POST','GET'])
def clac():
    if request.method == 'GET':
        return render_template('calculator.html',math='calculator',inptTxt='Enter Calculation Below:')

    else:
        session['calcInpt'] = request.form['input']
        num = math(session['calcInpt'],'c')
        flash(session['calcInpt'])
        flash(num)
        return render_template('calculator.html')


@math.route('/function', methods = ['POST','GET'])
def function():
    if request.method == 'GET':
        return render_template('calculator.html',math='Functions',inptTxt='Enter Expression Below')

    else:
        session['calcInpt'] = request.form['input']
        num = simplify(session['calcInpt'])
        flash(session['calcInpt'])
        flash(num)
        return render_template('calculator.html')