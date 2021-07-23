# weather_paper
基于树莓派zero+微雪 2.13v2水墨屏的天气显示小工具

[2.13inch e-Paper HAT 官方文档](https://www.waveshare.net/wiki/2.13inch_e-Paper_HAT)

按照官方的<RPI使用教程>点亮屏幕后就可以根据官方的示例代码进行修改了



关于自动运行

cron服务是linux的内置服务，但它不会开机自动启动。可以用以下命令启动和停止服务：

编辑crontable

~~~bash
service cron start
vim /etc/rsyslog.conf ## 取消 cron.* 的注释，开启 cron 日志
crontab -e
0 0 * * * ？ * cd ~ && python3 weather_paper/bin/weather.py >> ~/cron.log 2>&1
~~~

开启cron服务

~~~bash
service cron start
service cron restart
service cron stop
service cron status
systemctl is-enabled cron.service  --- 查看crond是否为开机自启动
systemctl enable cron.service  --- 将服务设置为开启启动
systemctl disable cron.service  --- 关闭服务开机自启动
~~~

关于时间同步

~~~bash
#安装NTP
sudo apt-get install ntpdate
#选择 上海时区
sudo dpkg-reconfigure tzdata
#同步时间
#添加到/etc/rc.local里面实现开机自启动
sudo ntpdate cn.pool.ntp.org
#查看当前时间
date
~~~

![img](\pic\IMG_20210723_140708.jpg)