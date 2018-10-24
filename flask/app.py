import random
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template


app = Flask(__name__)


def line_graph(file_name):
    df = pd.read_csv(file_name)
    p = figure(title="CO2 levels", x_axis_label='time', y_axis_label='CO2 ppm')
    p.line(df['time'], df['CO2-PPM'], line_width=2)
    return p


@app.route("/pi-CO2/<file_name>/")
def chart(file_name):
    # file_name = 'record.csv'
    p = line_graph(file_name)
    script, div = components(p)
    return render_template("chart.html",
                           the_div=div, the_script=script)


if __name__ == '__main__':
    app.run(debug=True)
