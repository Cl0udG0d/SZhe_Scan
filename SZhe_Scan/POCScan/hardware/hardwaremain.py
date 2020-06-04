#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: hardware漏洞库
referer: unknow
author: Lucifer
description: 包含所有hardware漏洞类型，封装成一个模块
'''

#router vulns
from POCScan.hardware.router.router_dlink_webproc_fileread import router_dlink_webproc_fileread_BaseVerify
from POCScan.hardware.router.router_dlink_command_exec import router_dlink_command_exec_BaseVerify
from POCScan.hardware.router.router_ruijie_unauth import router_ruijie_unauth_BaseVerify

#gateway vulns
from POCScan.hardware.gateway.adtsec_gateway_struts_exec import adtsec_gateway_struts_exec_BaseVerify
from POCScan.hardware.gateway.adtsec_Overall_app_js_bypass import adtsec_Overall_app_js_bypass_BaseVerify
from POCScan.hardware.gateway.mpsec_weakpass_exec import mpsec_weakpass_exec_BaseVerify
from POCScan.hardware.gateway.mpsec_webui_filedownload import mpsec_webui_filedownload_BaseVerify

#camera vulns
from POCScan.hardware.camera.camera_uniview_dvr_rce import camera_uniview_dvr_rce_BaseVerify
from POCScan.hardware.camera.camera_hikvision_web_weak import camera_hikvision_web_weak_BaseVerify

#printer vulns
from POCScan.hardware.printer.printer_xerox_default_pwd import printer_xerox_default_pwd_BaseVerify
from POCScan.hardware.printer.printer_hp_jetdirect_unauth import printer_hp_jetdirect_unauth_BaseVerify
from POCScan.hardware.printer.printer_topaccess_unauth import printer_topaccess_unauth_BaseVerify
from POCScan.hardware.printer.printer_canon_unauth import printer_canon_unauth_BaseVerify

#cannot import name 'spawn' from 'pexpect'
#发现该函数不能在 windows 系统下运行，换 linux 系统,在windows下注释掉。
#firewall vulns
# from hardware.firewall.juniper_netscreen_backdoor import juniper_netscreen_backdoor_BaseVerify