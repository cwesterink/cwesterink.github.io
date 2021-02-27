import base64
import io
from math import *
from icecream import ic
from flask import Blueprint, render_template, request, session, flash
from icecream import ic
from .forms import FunctionForm, CalculateMatrixForm, NewMatrixForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# import math functions
from .calculator import fx


math_bp = Blueprint('math_bp', __name__, static_folder='static', template_folder='templates')
math_bp.secret_key = "const"


@math_bp.route('/calculator', methods=['POST', 'GET'])
def calc():
    if request.method == 'POST':
        session['calcInpt'] = request.form['input']
        f = { 'cos': cos, 'tan': tan, 'sin': sin, 'sqrt': sqrt, 'pi': pi, "e": e, 'abs': fabs, "π": pi}
        try:
            num = eval(session['calcInpt'], f)
        except:
            num = 'error could not calculate'
        else:
            flash(session['calcInpt'])
            flash(session['calcInpt']+' = '+str(num))
    return render_template('calculator.html', math='Calculator', inptTxt='Enter Calculation Below:', extra='')


@math_bp.route('/function', methods=['POST', 'GET'])

def function():


    form = FunctionForm()
    if form.validate_on_submit():
        inpt = form.function.data
        color = form.color.data
        ranges = form.range.data
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

        return render_template('calculator.html', math='Function', form = form ,plt=image)

    return render_template('calculator.html', math='Function', form = form)




from .matrix import *
from .matrix import matrix
@math_bp.route('/matrix', methods=['POST','GET'])
def matrixR():
    # JINJA2 VARS
    answer = ""
    calcError = ""
    mtxError = ""

    # FORM INSTANCES
    newMtxform = NewMatrixForm()
    calcForm = CalculateMatrixForm()
    if request.method == "GET":
        session["matrix"] = dict()

        session['numMtx'] =0
        print(session)
    if request.method == "POST":

        if newMtxform.validate_on_submit():  # NEW MATRIX CREATED

            name = newMtxform.name.data  # GET NAME

            newMtx = newMtxform.new_matrix.data.split("\r\n")  # SPLIT INPUT INTO LIST
            for row in range(len(newMtx)):
                newMtx[row] = newMtx[row].split("|")
                for c in range(len(newMtx[row])):
                    newMtx[row][c] = int(newMtx[row][c])

            try:  # TEST TO SEE IF VALID

                x = matrix(newMtx)
                session['numMtx'] += 1
                session["matrix"].update({name:newMtx})
                ic(session)
            except:  # IS NOT VALID
                print("failed")
                mtxError = "Matrix is not Valid. Try again"

        if calcForm.validate_on_submit():  # MATRIX CALCULATION
            ic(session)
            import copy
            inpt = calcForm.inpt.data  # GET INPUT

            mFunctions = {"det": matrix.det, "cofactor": matrix.cofactor, "ajoint": matrix.ajoint,
                          "transpose": matrix.transpose, 'identity': identity}

            mtx = copy.deepcopy(session["matrix"])  # GET CREATED MATRICES

            for i in mtx.keys():  # ITERATE THROUGH DICT TRANSFORMING LIST TO MATRIX TYPES
                mtx[i] = matrix(mtx.get(i))

            mFunctions = mFunctions | mtx

            try:
                answer = eval(inpt, mFunctions)

            except(NameError):
                calcError = "matrix is not defined. Try Again"
                answer = ""

            else:

                try:
                    assert type(answer) == int or type(answer) == float or type(answer) == matrix

                except:

                    calcError = answer
                    answer = ""
                else:
                    if type(answer) == matrix:
                        answer = answer.toList()
                        s = "\r\n"
                        for row in answer:
                            for cell in row:
                                s += str(cell) + " "
                            s += "\r\n"
                        answer = s

    # answer = "hello \r\n bob \r\n bye"
    mats = list(session["matrix"].keys())

    return render_template('matrix.html', mats=mats, calcForm=calcForm, newMtxForm=newMtxform, calcError=calcError,
                           mtxError=mtxError, outPut=answer)



"""
    #JINJA2 VARS
    answer = ""
    calcError = ""
    mtxError = ""

    #FORM INSTANCES
    newMtxForm = NewMatrixForm()
    calcForm = CalculateMatrixForm()


    if request.method == "POST":
        ic("POST")
        ic(session)
        if newMtxForm.validate_on_submit(): #NEW MATRIX CREATED

            name = newMtxForm.name.data #GET NAME

            newMtx = newMtxForm.new_matrix.data.split("\r\n") #SPLIT INPUT INTO LIST
            for row in range(len(newMtx)):
                newMtx[row] = newMtx[row].split("|")
                for c in range(len(newMtx[row])):
                    newMtx[row][c] = int(newMtx[row][c])


            try: #TEST TO SEE IF VALID

                x = matrix(newMtx)
                ic(session)
                session["matrix"][name] = newMtx
                ic(session)

            except: #IS NOT VALID
                print("failed")
                mtxError = "Matrix is not Valid. Try again"

        if calcForm.validate_on_submit(): #MATRIX CALCULATION

            inpt = calcForm.inpt.data #GET INPUT

            mFunctions = {"det": matrix.det, "cofactor": matrix.cofactor, "ajoint": matrix.ajoint,
                          "transpose": matrix.transpose, 'identity': identity}



            mtx = copy.deepcopy(session["matrix"])#GET CREATED MATRIXCES

            for i in mtx.keys(): #ITERATE THROUGH DICT TRANSFORMING LIST TO MATRIX TYPES
                mtx[i] = matrix(mtx.get(i))

            mFunctions = mFunctions | mtx

            try:
                answer = eval(inpt, mFunctions)

            except(NameError):
                calcError = "matrix is not defined. Try Again"
                answer = ""

            else:

                try:
                    assert type(answer) == int or type(answer) == float or type(answer) == matrix

                except:

                    calcError = answer
                    answer = ""
                else:
                    if type(answer) == matrix:
                        answer = answer.toList()
                        s = "\r\n"
                        for row in answer:
                            for cell in row:
                                s += str(cell) + " "
                            s += "\r\n"
                        answer = s

    #mats = list(copy.deepcopy(session["matrix"]).keys())
    mats = list(session["matrix"].keys())
    ic(session)
    ic(mats)

    return render_template('matrix.html', mats=mats, calcForm=calcForm, newMtxForm=newMtxForm, calcError=calcError, mtxError = mtxError, outPut = answer)

"""

    
