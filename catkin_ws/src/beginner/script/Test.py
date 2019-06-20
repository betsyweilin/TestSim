#!/usr/bin/python2.7
#coding=utf-8
import string
import wx
import sys
import os
import thread
import time
import rospy
import yaml

from threading import Thread
from dashboard_msgs.msg  import RunConfig
from dashboard_msgs.msg  import LoadRet

import  threading


def load_yaml(filename, def_ret=None):
	dir = os.getcwd()
	path = dir + "/" + filename
	print path
	if not os.path.isfile(path):
		return def_ret
	print('loading ' + filename)
	f = open(filename, 'r')
	d = yaml.load(f)
	f.close()
	return d

class MyFrame(wx.Frame):
    def __init__(self,parent=None):
        super(MyFrame, self).__init__(parent,-1,"Control",size=(600,400))
        panel = wx.Panel(self,-1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vsizer)

        btn0 = wx.Button(panel,label="config")
        self.Bind(wx.EVT_BUTTON,self.OnClickConfig,btn0)
        btn0.SetDefault()

        btn1 = wx.Button(panel,label="prepare")
        self.Bind(wx.EVT_BUTTON,self.OnClickPrepare,btn1)
        #btn1.SetDefault()  #将按钮设置为默认按钮，不然会是选中状态，边框不同 

        btn2 = wx.Button(panel,label="starttest")
        self.Bind(wx.EVT_BUTTON,self.OnClickStart,btn2)
        btn2.SetDefault()  #将按钮设置为默认按钮，不然会是选中状态，边框不同
        #按顺序排列button
        vsizer.Add(btn0,0,wx.ALIGN_CENTER_HORIZONTAL)
        vsizer.Add(btn1,0,wx.ALIGN_CENTER_HORIZONTAL)
        vsizer.Add(btn2,0,wx.ALIGN_CENTER_HORIZONTAL)


	self.all_procs = []
	self.all_cmd_dics = []
	self.load_dic = self.load_yaml('param.yaml', def_ret={})

  	self.parseparm()
    def load_yaml(self, filename, def_ret=None):
        return load_yaml(filename, def_ret)

    def save_param_yaml(self):
	save_dic = {}
	for (name, pdic) in self.load_dic.items():
		if pdic and pdic != {}:
			prm = self.cfg_dic( {'name':name, 'pdic':pdic} ).get('param', {})
			no_saves = prm.get('no_save_vars', [])
			pdic = pdic.copy()
			for k in pdic.keys():
				if k in no_saves:
					del pdic[k]
			save_dic[name] = pdic

	names = []
	for proc in self.all_procs:
		(_, obj) = self.proc_to_cmd_dic_obj(proc)
		name = self.cfg_dic( { 'obj': obj } ).get('name')
		names.append(name)
	if 'booted_cmds' not in save_dic:
		save_dic['booted_cmds'] = {}
	save_dic.get('booted_cmds')['names'] = names

	if save_dic != {}:
		dir = rtmgr_src_dir()
		print('saving param.yaml')
		f = open(dir + 'param.yaml', 'w')
		s = yaml.dump(save_dic, default_flow_style=False)
		#print 'save\n', s # for debug
		f.write(s)
		f.close()

    def parseparm(self):

 	print " parse parm!"
    
    def OnClickStop(self, event):
 	print " stop!"

    def OnClickConfig(self,event):
        print "Config! "
	cfg=RunConfig()
        cfg.m_ncaseid=self.load_dic.get('ConfigRun')['m_ncaseid']
	cfg.m_nrunnum=self.load_dic.get('ConfigRun')['m_nrunnum']
	cfg.map_name=self.load_dic.get('ConfigRun')['map_name']
	cfg.host_name=self.load_dic.get('ConfigRun')['host_name']

	pub_cmd.publish(cfg)


    def OnClickPrepare(self,event):
        print "START! "


    def OnClickStart(self,event):
        print "START! "



    def OnClose(self, event):
        print "onclose! "
	self.Destroy()


def Sim_func_cb(data):

    if(data.m_nloadval == 0): 
        print ("simload is success" )

    else:
        print ("simload NOT success" )


def TestBoard_func_cb(data):

    if(data.m_nloadval == 0): 
        print ("simload is success" )

    else:
        print ("simload NOT success" )



if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()

    rospy.init_node('TestDemo', anonymous=False)
    pub_cmd = rospy.Publisher('TestDemo_Config', RunConfig, queue_size=10)
    sub = rospy.Subscriber('Sim_Return', LoadRet, Sim_func_cb) 
    sub = rospy.Subscriber('TestBoard_Return', LoadRet, TestBoard_func_cb) 

    app.MainLoop()

