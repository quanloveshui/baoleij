#!/usr/bin/env python

from backend import paramiko_ssh
from conf import settings



class SshHandler(object):
    """堡垒机交互脚本"""

    def __init__(self,argv_handler_instance):
        self.argv_handler_instance = argv_handler_instance
        #self.models = models



    def auth(self):
        """认证程序"""
        count = 0
        while count < 3:
            username = input("堡垒机账号:").strip()
            password = input("Password:").strip()
            if username in settings.userinfo.keys():
                if password==settings.userinfo[username]:
                    self.user = username
                    return True
                else:
                    print('账号或密码不对')
                    #return False
            else:
                print('账号或密码不对')
                #return False
            count+=1


    def interactive(self):
        """启动交互脚本"""
        if self.auth():
            print("Ready to print all the authorized hosts...to this user ...")
            while True:
                host_list = settings.host_dic[self.user].keys()
                host_list = list(host_list)
                for index,host in enumerate(host_list):
                    print("%s.\t%s"%(index,host))
                choice = input("请选择host>>:").strip()
                if choice.isdigit():
                    choice = int(choice)
                    print("going to logon  %s" % host_list[choice] )
                    paramiko_ssh.ssh_connect(self, host_list[choice])
