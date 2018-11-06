#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: exponentialSmoothing.py
@time: 2018/10/31 10:32
@function：指数平滑预测
"""
from datetime import datetime,timedelta
import pandas as pd


def read_excl():
    excel_path = '20-31.xls'
    df = pd.read_excel(excel_path)
    datas = list()
    append = datas.append
    for i in range(0, len(df)):
        meter = dict()
        meteraddr= str(df.iloc[i].get('表计表号'))
        meteraddr = meteraddr.rjust(12,'0')
        meter.setdefault('MeterAddr', meteraddr)
        meter.setdefault('DataTime',str(df.iloc[i].get('数据时间')))
        meter.setdefault('Value', float(df.iloc[i].get('电表余额')))
        append(meter)
    return datas

class ExponentialSmoothing:
    """
    指数平滑预测
    """

    def __init__(self,weight:float,datas:list):
        self._weight = weight
        self._datas = datas



    def start(self):
        """
        开始预测
        :return:
        """
        print('开始进行预测!')
        print('输入的数据为:',self._datas)
        if len(self._datas) <3:
            raise ValueError('预测数组长度不足,少于3个!')
        self._datas.sort(key=lambda x: x["DataTime"])

        initial = (self._datas[0].get('Value')+self._datas[1].get('Value')+self._datas[2].get('Value'))/3
        predicteds = dict()
        is_first =True
        last_predicted = None
        for data in self._datas:
            pre_time =data.get('DataTime') + timedelta(days=1)
            if is_first:
                value = self._weight * data.get('Value') + (1 - self._weight) * initial
                last_predicted = value
                is_first =False
            else:
                value = self._weight * data.get('Value') + (1 - self._weight) * last_predicted
                last_predicted = value
            predicteds.setdefault(pre_time.strftime('%Y-%m-%d'), value)
        last_second_predicteds = self._datas[1].get('Value')
        second_predicteds = dict()
        for k,v in predicteds.items():
            second_predicted = self._weight * v +(1-self._weight)*last_second_predicteds
            last_second_predicteds = second_predicted
            second_predicteds.setdefault(k,second_predicted)
        return predicteds,second_predicteds


if __name__ == '__main__':
    source = read_excl()
    datas =list()
    append = datas.append
    i =0
    weight = 0.6
    for d in source:
        if d.get('MeterAddr') == '521233302766':
            d['DataTime'] = datetime.strptime(d.get('DataTime'),'%Y-%m-%d %H:%M:%S')
            append(d)
            i+=1
    print('原始数据:',datas)
    if len(datas) >7 :
        pre_datas = datas[0:7]
    else:
        pre_datas = datas
    ex = ExponentialSmoothing(weight=weight,datas=pre_datas)
    predicteds, second_predicteds = ex.start()
    for data in pre_datas:
        print('{0}的实际值为{1}'.format(data.get('DataTime'),data.get('Value')))
        print('{0}的一次平滑为{1}'.format(data.get('DataTime'), predicteds.get(data.get('DataTime').strftime('%Y-%m-%d'))))
        print('{0}的二次平滑为{1}'.format(data.get('DataTime'), second_predicteds.get(data.get('DataTime').strftime('%Y-%m-%d'))))
    print()
    pre_day = datetime(2018,11,2)
    str_pre_day = pre_day.strftime('%Y-%m-%d')
    a = 2 * predicteds.get(str_pre_day) - second_predicteds.get(str_pre_day)
    c = predicteds.get(str_pre_day) - second_predicteds.get(str_pre_day)
    b = (weight/(1-weight))*c
    t = a + b * 1
    e = datas[-3].get('Value')
    print('实际值为',e)
    print('{0}的预测值:{1}'.format(str_pre_day,t))
    d = (t-e)/(e/100)
    print('误差值为',d)
    t = a + b * 2
    str_pre_day = (pre_day + timedelta(days=1)).strftime('%Y-%m-%d')
    print('{0}的预测值:{1}'.format(str_pre_day, t))
    t = a + b * 3
    str_pre_day = (pre_day + timedelta(days=2)).strftime('%Y-%m-%d')
    print('{0}的预测值:{1}'.format(str_pre_day, t))
    print()
    d = int(-a/b)
    print('还能用{0}天!'.format(d))