import base64

from flask import Blueprint, render_template, redirect, request, url_for, session, flash, make_response, Response

import matplotlib.pyplot as plt
import io

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# import math functions
from calculator import mathy
from calculator import fx

math_bp = Blueprint('math_bp', __name__, static_folder='static', template_folder='templates')


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
        axis.plot(x, y, color+"o")

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
    return render_template('matrix.html')
