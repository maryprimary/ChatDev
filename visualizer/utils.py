
import logging
import requests
import os
import pandas
import datetime
from matplotlib import pyplot

from visualizer.app import port

def visualize_dataframe(df: pandas.DataFrame, base: str):
    '''显示一个图'''
    if not os.path.exists('visualizer/__temp__'):
        os.mkdir('visualizer/__temp__')
    fig, ax = pyplot.subplots()
    df[base].plot(ax=ax)
    fname = datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')
    fig.savefig('visualizer/__temp__/{}.png'.format(fname))
    #PDFIGS.append('visualizer/__temp__/{}.png'.format(fname))
    try:
        data = {"fname": '__temp__/{}.png'.format(fname)}
        response = requests.post(f"http://127.0.0.1:{port[-1]}/append_pdfig", json=data)
    except:
        logging.info("flask app.py did not start for online log")
    #return send_from_directory("static", "visualize_dataframe.html")



def send_msg(role, text):
    try:
        data = {"role": role, "text": text}
        response = requests.post(f"http://127.0.0.1:{port[-1]}/send_message", json=data)
    except:
        logging.info("flask app.py did not start for online log")
