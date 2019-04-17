# -*- coding:utf-8 -*-

import ConfigParser
import os
import sys
import json
import urllib2
import requests
import sys

sys.path.append('..')
import PhoneCommon as Pho
import FunctionCommon as Fun


class STFDevicesControl:
    def __init__(self, sfile='stf.ini', conf_name='stfdevice'):
        self.url = ""
        self.access_token = ""
        self.api_token = ""
        self.__get_api_conf(sfile, conf_name)

    def __get_api_conf(self, sfile, conf_name):
        full_path = Fun.get_file_in_directory_full_path(sfile)
        print full_path
        if not os.path.exists(full_path):
            print("Error: Cannot get config file")
            sys.exit(-1)
        sfile = full_path
        conf = ConfigParser.ConfigParser()
        conf.read(sfile)
        print conf.sections()
        try:
            self.url = conf.get(conf_name, "url")
            self.access_token = conf.get(conf_name, "access_token")
            self.api_token = conf.get(conf_name, "api_token")
        except Exception, e:
            print("Error: " + str(e))
            sys.exit(-1)

    # 使用设备
    def add_user_devices(self, serial):
        # (url, access_token, api_token) = self.get_api_conf()
        api_url = self.url + "/api/v1/user/devices"
        token = self.access_token + " " + self.api_token

        data = {'serial': serial}
        request = urllib2.Request(api_url, json.dumps(data))
        request.add_header('Authorization', token)
        request.add_header('Content-Type', 'application/json')
        try:
            urllib2.urlopen(request)
        except Exception, e:
            print e.code
            print e.read()

    # 释放所有使用的设备
    def remove_devices_user(self, device_list):
        # (url, access_token, api_token) = self.get_api_conf("conf/stf.conf", "renguoliang")
        for device in device_list:
            serial = device["serial"]
            api_url = self.url + "/api/v1/user/devices/%s" % serial
            print api_url
            token = self.access_token + " " + self.api_token
            request = urllib2.Request(api_url)
            request.add_header('Authorization', token)
            request.get_method = lambda: 'DELETE'
            try:
                urllib2.urlopen(request)
            except Exception, e:
                print e.code
                print e.read()

    # 释放单个使用的设备
    def remove_device(self, serial):
        # (url, access_token, api_token) = self.get_api_conf("conf/stf.conf", "renguoliang")
        api_url = self.url + "/api/v1/user/devices/%s" % serial
        print api_url
        token = self.access_token + " " + self.api_token
        request = urllib2.Request(api_url)
        request.add_header('Authorization', token)
        request.get_method = lambda: 'DELETE'
        try:
            urllib2.urlopen(request)
        except Exception, e:
            print e.code
            print e.read()

    # 获取可用设备列表
    def get_devices_list(self):
        # (url, access_token, api_token) = self.get_api_conf("conf/stf.conf", "renguoliang")
        api_url = self.url + "/api/v1/devices"
        token = self.access_token + " " + self.api_token
        # 通过STF的API获取设备信息，并转换为json格式
        try:
            headers = {"Authorization": token}
            req = requests.get(api_url, headers=headers)
            # print req.text.encode('utf-8')
            req_dict = json.loads(json.dumps(req.json(), ensure_ascii=False, encoding='utf-8'))
        except Exception, e:
            print("Error: " + str(e))
            sys.exit(-1)
        device_list = req_dict["devices"]
        total_devices_num = len(device_list)
        device_status_list = []
        # 判断机器状态，判断规则见stf_status.mmap，来源于STF源码
        for device in device_list:
            if device['present']:
                if device['status'] == 3:
                    if device['ready']:
                        device_status_list.append(
                            {'serial': device['serial'].encode('utf-8'),
                             # ws://10.60.114.29:7548
                             'display_url': device['display']['url'].encode('utf-8'),
                             'manufacturer': device['manufacturer'].encode('utf-8'),
                             'using': device['using'],
                             'owner': device['owner'],
                             'model': device['model'].encode('utf-8'),
                             'version': device['version'].encode('utf-8'),
                             'apilevel': device['sdk'].encode('utf-8')})
        return device_status_list

    def get_remote_connect_url(self, serials):
        devices_list = self.get_devices_list()
        urls = dict()
        for device in devices_list:
            serial = device['serial']
            if device['serial'] not in serials:
                continue
                # display url "url": "ws://10.60.114.29:7564"
                # "remoteConnectUrl": "10.60.114.29:7565"
            display_url = device['display_url']
            if display_url is not None:
                display_url = display_url['ws://'.__len__():]
                sign_index = display_url.find(':')
                display_port = display_url[sign_index + 1:]
                ip = display_url[:sign_index]
                urls[serial] = ip + ':' + str((int(display_port) + 1))
        return urls


if __name__ == '__main__':
    sc = STFDevicesControl()
    print STFDevicesControl.get_devices_list(sc)
    # print sc.get_remote_connect_url(Pho.remote_devices)
    devices = sc.get_remote_connect_url(Pho.remote_devices)
    for k, d in devices.iteritems():
        print d
