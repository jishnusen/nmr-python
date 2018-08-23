from flask import Flask, jsonify, render_template, request

from io import BytesIO, StringIO
import base64

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import fortran_90_ports.bcsaxfort as b
import fortran_90_ports.q3q4stexfort as q3q4
import fortran_90_ports.qmasexfort as qmas
import fortran_90_ports.quadexfort as quad
import gauss as ga

app = Flask(__name__)


@app.route('/_bcsax')
def bcsax():
    plt.clf()
    f, g = b.bcsax(
        request.args.get('s11', 0, type=float),
        request.args.get('s22', 0, type=float),
        request.args.get('s33', 0, type=float),
        request.args.get('jfreq', 0, type=float),
        request.args.get('t2', 0, type=float),
        request.args.get('hi', 0, type=float),
        request.args.get('lo', 0, type=float),
        request.args.get('w0', 0, type=float))
    gen_data = plt.plot(f, g, label="Simulation")

    if request.args.get('hasexpdata', "", type=str) == "true":
        data = request.args.get('expdata', "", type=str)
        infile = np.genfromtxt(BytesIO(data.encode('utf-8')), delimiter=',')
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()

    image = BytesIO()

    plt.savefig(image, format='png')
    image_str = base64.b64encode(image.getvalue()).decode()
    html = '''data:image/png;base64,%s''' % (image_str)

    if request.args.get('save', "", type=str) == "true":
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        return jsonify(result=html, dwnld=csv)

    return jsonify(result=html)


@app.route('/bcsax')
def bcsax_form():
    return render_template('bcsax.html')


@app.route('/_q3q4stex')
def q3q4stex():
    plt.clf()
    f, g = q3q4.q3q4stex(
        request.args.get('vlf', 0, type=float),
        request.args.get('avspara', 0, type=float),
        request.args.get('avsperp', 0, type=float),
        request.args.get('ncth', 0, type=float),
        request.args.get('jfreq', 0, type=float),
        request.args.get('t2', 0, type=float),
        request.args.get('hi', 0, type=float),
        request.args.get('lo', 0, type=float),
        request.args.get('posq4', 0, type=float))
    gen_data = plt.plot(f, g, label="Simulation")

    if request.args.get('hasexpdata', "", type=str) == "true":
        data = request.args.get('expdata', "", type=str)
        infile = np.genfromtxt(BytesIO(data.encode('utf-8')), delimiter=',')
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()

    image = BytesIO()

    plt.savefig(image, format='png')
    image_str = base64.b64encode(image.getvalue()).decode()
    html = '''data:image/png;base64,%s''' % (image_str)

    if request.args.get('save', "", type=str) == "true":
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        return jsonify(result=html, dwnld=csv)

    return jsonify(result=html)


@app.route('/q3q4stex')
def q3q4stex_form():
    return render_template('q3q4stex.html')


@app.route('/_gauss')
def gauss():
    plt.clf()
    f, g = ga.run(
        request.args.get('vlf', 0, type=float),
        request.args.get('pos', "", type=str),
        request.args.get('inp', "", type=str),
        request.args.get('lo', 0, type=float),
        request.args.get('hi', 0, type=float),
        request.args.get('t2', 0, type=float),
        request.args.get('jfreq', 0, type=float))
    gen_data = plt.plot(f, g, label="Simulation")

    if request.args.get('hasexpdata', "", type=str) == "true":
        data = request.args.get('expdata', "", type=str)
        infile = np.genfromtxt(BytesIO(data.encode('utf-8')), delimiter=',')
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()

    image = BytesIO()

    plt.savefig(image, format='png')
    image_str = base64.b64encode(image.getvalue()).decode()
    html = '''data:image/png;base64,%s''' % (image_str)

    if request.args.get('save', "", type=str) == "true":
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        return jsonify(result=html, dwnld=csv)

    return jsonify(result=html)


@app.route('/gauss')
def gauss_form():
    return render_template('gauss.html')


@app.route('/_qmasex')
def qmasex():
    plt.clf()
    f, g = qmas.qmasex(
        request.args.get('sqn', 0, type=float),
        request.args.get('vlf', 0, type=float),
        request.args.get('eta1', 0, type=float),
        request.args.get('eqqh1', 0, type=float),
        request.args.get('cs1', 0, type=float),
        request.args.get('t2one', 0, type=float),
        request.args.get('npolar1', 0, type=float),
        request.args.get('nazim1', 0, type=float),
        request.args.get('eta2', 0, type=float),
        request.args.get('eqqh2', 0, type=float),
        request.args.get('cs2', 0, type=float),
        request.args.get('t2two', 0, type=float),
        request.args.get('npolar2', 0, type=float),
        request.args.get('nazim2', 0, type=float),
        request.args.get('hi', 0, type=float),
        request.args.get('lo', 0, type=float),
        request.args.get('jfreq', 0, type=float))
    gen_data = plt.plot(f, g, label="Simulation")

    if request.args.get('hasexpdata', "", type=str) == "true":
        data = request.args.get('expdata', "", type=str)
        infile = np.genfromtxt(BytesIO(data.encode('utf-8')), delimiter=',')
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()

    image = BytesIO()

    plt.savefig(image, format='png')
    image_str = base64.b64encode(image.getvalue()).decode()
    html = '''data:image/png;base64,%s''' % (image_str)

    if request.args.get('save', "", type=str) == "true":
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        return jsonify(result=html, dwnld=csv)

    return jsonify(result=html)


@app.route('/qmasex')
def qmasex_form():
    return render_template('qmasex.html')


@app.route('/_quadex')
def quadex():
    plt.clf()
    f, g = quad.quadex2(
        request.args.get('sqn', 0, type=float),
        request.args.get('vlf', 0, type=float),
        request.args.get('eta1', 0, type=float),
        request.args.get('eqqh1', 0, type=float),
        request.args.get('cs1', 0, type=float),
        request.args.get('t2one', 0, type=float),
        request.args.get('npolar1', 0, type=float),
        request.args.get('nazim1', 0, type=float),
        request.args.get('eta2', 0, type=float),
        request.args.get('eqqh2', 0, type=float),
        request.args.get('cs2', 0, type=float),
        request.args.get('t2two', 0, type=float),
        request.args.get('npolar2', 0, type=float),
        request.args.get('nazim2', 0, type=float),
        request.args.get('hi', 0, type=float),
        request.args.get('lo', 0, type=float),
        request.args.get('jfreq', 0, type=float))
    gen_data = plt.plot(f, g, label="Simulation")

    if request.args.get('hasexpdata', "", type=str) == "true":
        data = request.args.get('expdata', "", type=str)
        infile = np.genfromtxt(BytesIO(data.encode('utf-8')), delimiter=',')
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()

    image = BytesIO()

    plt.savefig(image, format='png')
    image_str = base64.b64encode(image.getvalue()).decode()
    html = '''data:image/png;base64,%s''' % (image_str)

    if request.args.get('save', "", type=str) == "true":
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        return jsonify(result=html, dwnld=csv)

    return jsonify(result=html)


@app.route('/quadex')
def quadex_form():
    return render_template('quadex.html')


if __name__ == "__main__":
    app.run()
