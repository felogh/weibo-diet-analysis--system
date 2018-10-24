# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, Response, json, jsonify
import draw
import os
import draw_foods
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg

__all__ = ['app']

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    首页： 通过地区，性别，时间，方式进行搜索
    :return: 搜索页，Ajax显示结果
    """
    if request.method == 'GET':
        return render_template('index.html')
    else:
        district = request.values.get('district')
        gender = request.values.get('gender')
        time = request.values.get('time')
        mode = request.values.get('mode')
        print(district, gender, time, mode)

        # 采用savefig的方式
        pathtf = './static/img/topfoods/' + 'd' + district + '_g' + gender + '_t' + time + '_m' + mode + '.png'
        pathwc = './static/img/wordcloud/' + 'd' + district + '_g' + gender + '_t' + time + '_m' + mode + '.png'
        if not os.path.exists(pathtf):
            draw.main(district, gender, time, mode)
        return pathtf + '#' + pathwc

        # 直接画图，但是被覆盖了
        # fig_tf, fig_wc = draw.main(district, gender, time, mode)
        #
        # buf_tf = BytesIO()
        # fig_tf.savefig(buf_tf, format='png')
        # data_tf = base64.encodebytes(buf_tf.getvalue()).decode()
        #
        # buf_wc = BytesIO()
        # fig_wc.savefig(buf_wc, format='png')
        # data_wc = base64.encodebytes(buf_wc.getvalue()).decode()
        #
        # data = 'data:image/png;base64,{}'.format(data_tf) + '#' + 'data:image/png;base64,{}'.format(data_wc)
        # print(data_tf == data_wc)
        # return data


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    食物搜索：通过食物进行搜索
    :return: 搜索页，Ajax显示结果
    """
    if request.method == 'GET':
        return render_template('search.html')
    else:
        food_name = request.values.get('food_name')
        choice = request.values.get('choice')
        print(food_name, choice)

        path = './static/img/food/' + food_name + '_' + choice +'.png'
        if not os.path.exists(path):
            draw_foods.main(food_name, choice)

        return path
        # fig = draw_foods.main(food_name, choice)
        # buf = BytesIO()
        # fig.savefig(buf, format='png')
        # data = base64.encodebytes(buf.getvalue()).decode()
        # return 'data:image/png;base64,{}'.format(data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
