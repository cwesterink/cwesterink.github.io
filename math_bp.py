from flask import Blueprint, render_template, redirect, request, url_for, session, flash, make_response, Response
from flask_sqlalchemy import SQLAlchemy

import base64
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from matrix import isValid
from matrix import calcMatrix

# import math functions
from calculator import mathy
from calculator import fx

math_bp = Blueprint('math_bp', __name__, static_folder='static', template_folder='templates')
math_bp.secret_key = "const"


@math_bp.route('/calculator', methods=['POST', 'GET'])
def calc():
    if request.method == 'POST':
        session['calcInpt'] = request.form['input']
        num = mathy(session['calcInpt'])
        flash(session['calcInpt'])
        flash(session['calcInpt']+' = '+str(num))
    return render_template('calculator.html', math='Calculator', inptTxt='Enter Calculation Below:', extra='')


@math_bp.route('/function', methods=['POST', 'GET'])


def function():

    if request.method == 'POST':
        inpt = str(request.form['input'])
        color = str(request.form['color'])
        ranges = int(request.form['range'])
        x, y = fx(inpt, ranges)

        # Generate plot
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("f(x)="+inpt)
        axis.set_xlabel("x")
        axis.set_ylabel("y")
        axis.grid()
        axis.plot(x, y, color+"-")

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        image = "data:image/png;base64,"
        image += base64.b64encode(pngImage.getvalue()).decode('utf8')

        return render_template('calculator.html', math='Function', plt=image)

    return render_template('calculator.html', math='Function')






@math_bp.route('/matrix', methods=['POST','GET'])
def matrix():
    if request.method == "POST":
        if 'matrix' in request.form and request.form['name'].isalpha():
        
            inp = str(request.form['matrix'])
            name = str(request.form['name'])
            m = session['m']
            if isValid(name,inp,m):
                
                m = session['m']
                print(type(m))
                m[name] = inp
                session['m'] = m
                print(session['m'])

            else:
                flash('Error found. Try again')
                
            return render_template('matrix.html', mats = session['m'], r = 'False')
        elif 'calculation' in request.form:
            expression = str(request.form['calculation'])
            
            try:
                answer, a, b, x = calcMatrix(expression,session['m'])

                return render_template('matrix.html', mats = session['m'], a = a, b = b, x = [x] , answer = answer, r = 'True')
            except:
                flash('calcMatrix error')
                return render_template('matrix.html', mats = session['m'], r = 'False')

            
            
            #return render_template('matrix.html', mats = session['m'], inpt = [a,b]  , answer = answer)

        else:
            flash('u need to entrer something')
            return render_template('matrix.html', mats = session['m'], r = 'False')

            

        
    else:
        
        
        session['m'] = dict()
        return render_template('matrix.html',r = 'False')
    
