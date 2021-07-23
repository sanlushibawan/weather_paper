#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import requests
import json

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def getNow():
    response = requests.get('http://d1.weather.com.cn/sk_2d/"你的城市代码".html') #例如北京-->101010100
    response.encoding = 'utf-8'
    jsons = json.loads(response.text[11:])
    return jsons



def weather_work():
    url = 'http://wthrcdn.etouch.cn/weather_mini?city="城市名称"' #例如 "北京"
    f=requests.get(url)
    f.encoding = 'utf-8'
    jsons=json.loads(f.text)
    return jsons['data']['forecast'][1:]


def get_pic_name(key):
    #weather pic
    pic_array = ['sun2.bmp','rain.bmp','cloud.bmp','sun_cloud.bmp']
    
    pic_name = 'sun2.bmp'
    if key == '晴':
        pic_name = pic_array[0]
    elif key == '多云':
        pic_name = pic_array[3]
    elif key == '阴':
        pic_name = pic_array[2]
    elif key.find('雨') != -1:
        pic_name = pic_array[1]
    else:
        pic_name = pic_array[0]
    return pic_name    



try:
    print('开始更新天气情况.....')
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
   
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.line([(81,0),(81,epd.height)],fill = 0,width = 2)
    json_sk = getNow()
    draw.text((36, 10), json_sk['weather'],font = font15,fill=0)
    draw.text((10, 36), json_sk['temp']+'°C',font = font24,fill=0)
    draw.line([(0,66),(81,66)],fill = 0 ,width = 1) 
    draw.text((0, 67), json_sk['WD'],font = font12,fill=0)
    draw.text((28, 67), json_sk['wse'],font = font12,fill=0)
    draw.text((0, 80), '湿度',font = font12,fill=0)
    draw.text((28, 80), json_sk['SD'],font = font12,fill=0)
    draw.text((10, 93), json_sk['date'][0:6],font = font12,fill=0)
    draw.text((5, 106),json_sk['date'][6:] + json_sk['time'],font = font12,fill=0)
    pic_name  = get_pic_name(json_sk['weather'])
    bmp = Image.open(os.path.join(picdir,pic_name))
    image.paste(bmp,(0,0))
    draw.line([(165,0),(165,epd.height)],fill = 0 ,width = 1)
    # Drawing next days x=83
    x1 = 83
    json_next = weather_work()
    json0 = json_next[0]
    draw.text((x1+11,10),json0['date'],font = font12,fill=0)
    image.paste(Image.open(os.path.join(picdir, get_pic_name(json0['type']))),(x1+23,23))
    #show weather type in center
    newx = x1
    lenx = 82 - (len(json0['type'])*15)
    if lenx > 0:
        newx = newx+(lenx/2)
    draw.text((newx,62),json0['type'],font = font15,fill = 0)
    draw.text((x1+23,78),json0['high'],font = font12,fill =0)
    draw.text((x1+23,91),json0['low'],font = font12,fill =0)
    draw.text((x1+23,104),json0['fengxiang'],font = font12,fill =0)
    # drawing nex days x = 165
    x1 = 165
    json_next = weather_work()
    json1 = json_next[1]
    draw.text((x1+11,10),json1['date'],font = font12,fill=0)
    image.paste(Image.open(os.path.join(picdir, get_pic_name(json1['type']))),(x1+23,23))
    #show weather type in center
    newx = x1
    lenx = 82 - (len(json1['type'])*15)
    if lenx > 0:
        newx = newx+(lenx/2)
    draw.text((newx,62),json1['type'],font = font15,fill = 0)
    draw.text((x1+23,78),json1['high'],font = font12,fill =0)
    draw.text((x1+23,91),json1['low'],font = font12,fill =0)
    draw.text((x1+23,104),json1['fengxiang'],font = font12,fill =0)
    #show & sleep e-paper
    epd.display(epd.getbuffer(image))
    epd.sleep()


        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()



