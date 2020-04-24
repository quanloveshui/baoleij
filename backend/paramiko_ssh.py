#!/usr/bin/env python



#paramiko源码中demo例子

import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback
from paramiko.py3compat import input
from conf import settings

import paramiko
try:
    import interactive
except ImportError:
    from . import interactive


def manual_auth(t,hostname,username, password):
    default_auth = 'p'
    #auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    # if len(auth) == 0:
    #     auth = default_auth
    auth = default_auth
    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        path = input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    elif auth == 'd':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
        path = input('DSS key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('DSS key password: ')
            key = paramiko.DSSKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    else:
        #pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        t.auth_password(username, password)


def ssh_connect(ssh_handler_instance,host):
    hostname = host
    port = settings.host_dic[ssh_handler_instance.user][host]['port']
    username = settings.host_dic[ssh_handler_instance.user][host]['user']
    password = settings.host_dic[ssh_handler_instance.user][host]['passwd']
    #print(">>>>>>>",username,password,host)

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if hostname not in keys:
            print('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[hostname]:
            print('*** WARNING: Unknown host key!')
        elif keys[hostname][key.get_name()] != key:
            print('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            print('*** Host key OK.')


        if not t.is_authenticated():
            manual_auth(t,hostname,username, password)
        if not t.is_authenticated():
            print('*** Authentication failed. :(')
            t.close()
            sys.exit(1)
        chan = t.open_session()#连接成功后打开一个channel
        chan.get_pty()#打开远程的terminal
        chan.invoke_shell()#激活terminal,然后就可以通过chan.send('command')和chan.recv(recv_buffer)来远程执行命令以及本地获取反馈

        chan.crazyeye_account = ssh_handler_instance.user
        chan.host_to_user = username
        #chan.models = ssh_handler_instance.models
        print('*** Here we go!\n')
        #写入数据库
        #ssh_handler_instance.models.AuditLog.objects.create(
        #    user = ssh_handler_instance.user ,
        #    log_type = 0 ,
        #    host_to_remote_user = host_to_user_obj,
        #    content = "***user login***"
        #)

        interactive.interactive_shell(chan)
        chan.close()
        t.close()
        #写入数据库
        #ssh_handler_instance.models.AuditLog.objects.create(
        #    user=ssh_handler_instance.user,
        #    log_type=2,
        #    host_to_remote_user=host_to_user_obj,
        #    content="***user logout***"
        #)

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)
