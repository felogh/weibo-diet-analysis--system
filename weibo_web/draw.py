# -*- coding: utf-8 -*-
import json
import copy
import matplotlib.pyplot as plt
from wordcloud import WordCloud

data_set = []
data_set_temp = []


# 读取数据
def open_file():
    global data_set
    with open('./data/weibo.json', 'rb') as f:
        for line in f:
            item = json.loads(line)
            data_set.append(item)
    clean_data()


# 清洗数据：去除不含食物的item
def clean_data():
    global data_set, data_set_temp
    for item in data_set:
        if len(item['food']) != 0:
            data_set_temp.append(item)
    data_set = copy.deepcopy(data_set_temp)
    del data_set_temp[:]


# 进行数据处理
def analysis(district='', gender='', time='', mode=''):
    global data_set, data_set_temp

    # 选择地点
    if district != '':
        for item in data_set:
            if len(item) == 10:
                continue
            if item['district'] == district:
                data_set_temp.append(item)
        data_set = copy.deepcopy(data_set_temp)
        del data_set_temp[:]

    # 选择性别
    if gender != '':
        for item in data_set:
            if item['user_gender'] == gender:
                data_set_temp.append(item)
        data_set = copy.deepcopy(data_set_temp)
        del data_set_temp[:]

    # 选择时间
    if time != '':
        for item in data_set:
            posted_at = determine_time(int(item['posted_at'][-5:-3]))
            if posted_at == time:
                data_set_temp.append(item)
        data_set = copy.deepcopy(data_set_temp)
        del data_set_temp[:]

    # 选择设备
    # 设备相关代码
    if mode != '':
        for item in data_set:
            posted_from = determine_mode(item['posted_from'])
            if posted_from == mode:
                data_set_temp.append(item)
        data_set = copy.deepcopy(data_set_temp)
        del data_set_temp[:]

    pathtf = './static/img/topfoods/' + 'd' + district + '_g' + gender + '_t' + time + '_m' + mode + '.png'
    pathwc = './static/img/wordcloud/' + 'd' + district + '_g' + gender + '_t' + time + '_m' + mode + '.png'
    # 作图
    # top食物
    # fig_tf = top_foods()
    top_foods(pathtf)

    # 词云
    # fig_wc = word_cloud()
    word_cloud(pathwc)

    # return fig_tf, fig_wc
    # return pathtf, pathwc


# 判断时间时间段
def determine_time(time):
    if 0 <= time <= 6:
        return 'midnight'
    elif 7 <= time <= 10:
        return 'forenoon'
    elif 11 <= time <= 13:
        return 'noon'
    elif 14 <= time <= 18:
        return 'afternoon'
    elif 19 <= time <= 23:
        return 'night'


# 判断发送方式
def determine_mode(mode):
    if mode is None:
        return '其它'
    elif 'iPhone' in mode:
        return 'iPhone'
    elif 'iPad' in mode:
        return 'iPad'
    elif 'Android' in mode:
        return 'Android'
    elif '小米' in mode or '红米' in mode:
        return '小米'
    elif 'OPPO' in mode:
        return 'OPPO'
    elif 'vivo' in mode:
        return 'vivo'
    elif '魅族' in mode or '魅蓝' in mode or 'MEIZU' in mode or 'Flyme' in mode:
        return '魅族'
    elif '华为' in mode or 'HUAWEI' in mode or '麦芒' in mode:
        return '华为'
    elif '荣耀' in mode:
        return '荣耀'
    elif '金立' in mode or '8848' in mode:
        return '金立'
    elif '乐视' in mode or '乐 ' in mode or '乐Pro' in mode or '乐1' in mode or '乐2' in mode or '乐M' in mode or \
            'Le' in mode:
        return '乐视'
    elif '360' in mode:
        return '360'
    elif 'nubia' in mode or '努比亚' in mode:
        return 'nubia'
    elif '三星' in mode or 'Samsung' in mode or 'GALAXY' in mode:
        return '三星'
    elif 'Nokia' in mode or 'Lumia' in mode:
        return 'Nokia'
    elif '中兴' in mode or 'ZTE' in mode:
        return '中兴'
    elif '美图' in mode:
        return '美图'
    elif 'Moto' in mode:
        return '摩托罗拉'
    elif '坚果' in mode or 'Smartisan' in mode or '堅果' in mode:
        return '锤子'
    elif 'OnePlus' in mode or '一加' in mode:
        return '一加'
    elif '联想' in mode:
        return '联想'
    elif 'Google' in mode or 'Nexus' in mode:
        return 'Google'
    elif 'HTC' in mode:
        return 'HTC'
    elif '索尼' in mode:
        return '索尼'
    elif '酷派' in mode:
        return '酷派'
    elif '微博' in mode or 'wei' in mode or 'Wei' in mode:
        return '微博相关平台'
    else:
        return '其它'


# 词云
def word_cloud(path):
    foods = ''

    for item in data_set:
        for food in item['food']:
            foods += food
            foods += '\n'

    wordcloud = WordCloud(background_color="white",
                          width=1000,
                          height=860,
                          margin=2,
                          font_path=r'C:\Windows\Fonts\msyh.ttc',
                          max_words=200).generate(foods)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.title('词云')

    plt.savefig(path)
    plt.gcf().clf()
    # fig = plt.gcf()
    # return fig


# top食物
def top_foods(path):
    top = 10
    foods_list = {}
    for item in data_set:
        for food in item['food']:
            if food in foods_list:
                foods_list[food] += 1
            else:
                foods_list[food] = 1

    # 排序
    foods_list = sorted(foods_list.items(), key=lambda d: d[1], reverse=True)

    # 画图
    xticks = []
    height = []
    bar_width = 0.3
    for times in range(top):
        xticks.append(foods_list[times][0])
        height.append(foods_list[times][1])
    plt.bar(range(top), height=height, width=bar_width)
    plt.xticks(range(top), xticks)
    plt.title('top食物')
    plt.savefig(path)
    plt.gcf().clf()
    # fig = plt.gcf()
    # return fig


# 主流程
def main(district=None, gender=None, time=None, mode=None):
    open_file()
    analysis(district, gender, time, mode)


if __name__ == '__main__':
    main()
