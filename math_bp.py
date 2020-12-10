from flask import Blueprint, render_template, redirect, request, url_for, session, flash
math_bp = Blueprint('math_bp', __name__, static_folder='static', template_folder='templates')


from calculator import mathy


@math_bp.route('/calculator', methods = ['POST','GET'])
def clac():
    if request.method == 'POST':

  
        session['calcInpt'] = request.form['input']
        num = mathy(session['calcInpt'])
        flash(session['calcInpt'])
        flash(num)
    return render_template('calculator.html',math='calculator',inptTxt='Enter Calculation Below:',extra='')


@math_bp.route('/function', methods = ['POST','GET'])
def function():
    if request.method == 'POST':
        
        session['calcInpt'] = request.form['input']
        print(session['calcInpt'])
        num = simplify(session['calcInpt'])
        flash(session['calcInpt'])
        flash(num)
    return render_template('calculator.html',math='Functions',inptTxt='Enter Expression Below',extra='f(x)=')