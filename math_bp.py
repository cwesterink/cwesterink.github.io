from flask import Blueprint, render_template, redirect, request, url_for, session, flash

math_bp = Blueprint('math_bp', __name__, static_folder='static', template_folder='templates')
import matplotlib.pyplot as plt

from calculator import mathy
from calculator import fx


@math_bp.route('/calculator', methods=['POST', 'GET'])
def clac():
    if request.method == 'POST':
        session['calcInpt'] = request.form['input']
        num = mathy(session['calcInpt'])
        flash(session['calcInpt'])
        flash(num)
    return render_template('calculator.html', math='Calculator', inptTxt='Enter Calculation Below:', extra='')


@math_bp.route('/function', methods=['POST', 'GET'])
def function():
    if request.method == 'POST':
        session['calcInpt'] = request.form['input']
        print(session['calcInpt'])
        x, y = fx(session['calcInpt'])
        flash(x)
        flash(y)
        plt.scatter(x, y)

        plt.grid()
        #plt.show()
        plt.savefig('cwesterink.github.io/static/plt.png')  # save the figure to file
        plt.close(plt)
    return render_template('calculator.html', math='Function', inptTxt='Enter Expression Below', extra='f(x)=')
