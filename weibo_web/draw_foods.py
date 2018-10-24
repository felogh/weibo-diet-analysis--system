# -*- coding: utf-8 -*-
import json
import copy
import matplotlib.pyplot as plt
from wordcloud import WordCloud

data_set = []
data_set_temp = []


class Type(object):
    # 男女比例
    @classmethod
    def gender_ratio(cls, path):
        path += 'gender_ratio.png'
        male = 0
        female = 0

        for item in data_set:
            if item['user_gender'] == 'male':
                male += 1
            elif item['user_gender'] == 'female':
                female += 1

        # 画图
        labels = ['男', '女']
        x = [male, female]
        explode = [0, 0.1]
        plt.pie(x, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True, labeldistance=1.1, startangle=90,
                pctdistance=0.6)
        plt.title('男女比例')

        plt.savefig(path)
        plt.gcf().clf()

    # 地理位置
    @classmethod
    def geo_dis(cls, path):
        path += 'geo_dis.png'
        district = {}
        xticks = []
        height = []

        for item in data_set:
            if len(item) == 10:
                continue
            if item['district'] in district:
                district[item['district']] += 1
            else:
                district[item['district']] = 1

        for dis in district:
            xticks.append(dis)
            height.append(district[dis])

        # 画图
        bar_width = 0.5
        plt.bar(range(len(district)), height=height, width=bar_width)
        plt.xticks(range(len(district)), xticks)
        plt.title('地理分布')
        plt.gcf().set_figwidth(18)

        plt.savefig(path)
        plt.gcf().clf()

    # 发送时段
    @classmethod
    def post_at(cls, path):
        path += 'post_at.png'
        section = {'forenoon': 0, 'noon': 0, 'afternoon': 0, 'night': 0, 'midnight': 0}
        for item in data_set:
            time = cls.determine_time(int(item['posted_at'][-5:-3]))
            section[time] += 1

        # 画图
        labels = ['上午/早上', '中午', '下午', '晚上', '夜间']
        x = [section['forenoon'], section['afternoon'], section['noon'], section['night'], section['midnight']]
        explode = [0, 0.1, 0, 0, 0]
        plt.pie(x, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True, labeldistance=1.1, startangle=90,
                pctdistance=0.6)
        plt.title('发送时段')

        plt.savefig(path)
        plt.gcf().clf()

    # 发送方式
    @classmethod
    def post_from(cls, path):
        path += 'post_from.png'
        mode_dic = {}
        xticks = []
        height = []
        for item in data_set:
            mode = cls.determine_mode(item['posted_from'])
            if mode in mode_dic:
                mode_dic[mode] += 1
            else:
                mode_dic[mode] = 1
        for mode in mode_dic:
            xticks.append(mode)
            height.append(mode_dic[mode])

        # 画图
        bar_width = 0.5
        plt.bar(range(len(mode_dic)), height=height, width=bar_width)
        plt.xticks(range(len(mode_dic)), xticks)
        plt.title('发送方式')
        plt.gcf().set_figwidth(15)

        plt.savefig(path)
        plt.gcf().clf()

    # 判断时间时间段
    @staticmethod
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
    @staticmethod
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
            return '微博相关'
        else:
            return '其它'


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
def analysis(food='', choice=''):
    global data_set, data_set_temp
    base_path = './static/img/food/' + food + '_'

    for item in data_set:
        if food in item['food']:
            data_set_temp.append(item)
    data_set = copy.deepcopy(data_set_temp)
    del data_set_temp[:]

    # 作图
    func = getattr(Type, choice)
    func(base_path)


# 主流程
def main(food='', choice=''):
    open_file()
    analysis(food, choice)


if __name__ == '__main__':
    main('苹果', 'post_from')
