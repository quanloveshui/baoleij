"""
说明：

实现堡垒机后端功能
登录堡垒机后启动脚本python bin.py  run
(如果想实现用户登录堡垒机后就自动执行脚本，可以在堡垒机用户家目录下的文件中添加执行脚本命令即可
及在/home/test/.bashrc中新增python /opt/baoleiji/crazyeye_manager.py run即可
)
可以看到该堡垒机账号授权的主机列表
选择主机列表连接远程主机后即可执行命令

"""




启动脚本
python bin.py  run

执行过程：

[root@master]# python bin.py  run   


堡垒机账号:test
Password:123456
Ready to print all the authorized hosts...to this user ...
0.      192.168.149.129
1.      192.168.149.128
2.      192.168.149.127
请选择host>>:0
going to logon  192.168.149.129
*** Host key OK.
*** Here we go!

Last login: Fri Apr 24 01:50:47 2020 from master
[test@master ~]$

已经成功连接远程主机可以执行命令

执行过的命令会记录在ssh_test.log
2020-04-24 08:54:05   lll
2020-04-24 08:54:06   ll
2020-04-24 08:54:08   exit
