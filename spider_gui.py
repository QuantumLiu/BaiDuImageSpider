# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\pyprojects\bdimgspider\gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys, os,re,urllib,traceback
from multiprocessing import Pool,cpu_count,freeze_support
import requests
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from spider import *

class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form,self).__init__()
        self.urls=[]
        self.nb_jobs=cpu_count()
        self.max_num=1000
        self.start_page=1
        self.dirname=''
        self.word=''
        pass

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 180)
        Form.setWindowIcon(QtGui.QIcon('./cat.ico'))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_key = QtWidgets.QLabel(Form)
        self.label_key.setAlignment(QtCore.Qt.AlignCenter)
        self.label_key.setWordWrap(False)
        self.label_key.setOpenExternalLinks(False)
        self.label_key.setObjectName("label_key")
        self.gridLayout.addWidget(self.label_key, 0, 0, 1, 1)
        self.edit_key = QtWidgets.QLineEdit(Form)
        self.edit_key.setObjectName("edit_key")
        self.gridLayout.addWidget(self.edit_key, 0, 1, 1, 3)
        self.bt_crawl = QtWidgets.QPushButton(Form)
        self.bt_crawl.setObjectName("bt_crawl")
        self.bt_crawl.clicked.connect(self.crawl)
        self.gridLayout.addWidget(self.bt_crawl, 0, 6, 1, 1)
        self.label_dir = QtWidgets.QLabel(Form)
        self.label_dir.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dir.setObjectName("label_dir")
        self.gridLayout.addWidget(self.label_dir, 1, 0, 1, 1)
        self.edit_dir = QtWidgets.QLineEdit(Form)
        self.edit_dir.setObjectName("edit_dir")
        self.gridLayout.addWidget(self.edit_dir, 1, 1, 1, 3)
        self.bt_select = QtWidgets.QPushButton(Form)
        self.bt_select.setObjectName("bt_select")
        self.bt_select.clicked.connect(self.select_dir)
        self.gridLayout.addWidget(self.bt_select, 1, 6, 1, 1)
        self.label_start = QtWidgets.QLabel(Form)
        self.label_start.setAlignment(QtCore.Qt.AlignCenter)
        self.label_start.setObjectName("label_start")
        self.gridLayout.addWidget(self.label_start, 2, 0, 1, 1)
        self.spin_start = QtWidgets.QSpinBox(Form)
        self.spin_start.setObjectName("spin_start")
        self.spin_start.setRange(1,2000)
        self.spin_start.setValue(1)
        self.gridLayout.addWidget(self.spin_start, 2, 1, 1, 1)
        self.label_max = QtWidgets.QLabel(Form)
        self.label_max.setAlignment(QtCore.Qt.AlignCenter)
        self.label_max.setObjectName("label_max")
        self.gridLayout.addWidget(self.label_max, 2, 2, 1, 1)
        self.spin_max = QtWidgets.QSpinBox(Form)
        self.spin_max.setObjectName("spin_max")
        self.spin_max.setRange(100,10**6)
        self.spin_max.setValue(100)
        self.gridLayout.addWidget(self.spin_max, 2, 3, 1, 1)
        self.label_jobs = QtWidgets.QLabel(Form)
        self.label_jobs.setAlignment(QtCore.Qt.AlignCenter)
        self.label_jobs.setObjectName("label_jobs")
        self.gridLayout.addWidget(self.label_jobs, 2, 4, 1, 1)
        self.spin_jobs = QtWidgets.QSpinBox(Form)
        self.spin_jobs.setObjectName("spin_jobs")
        self.spin_jobs.setRange(1,cpu_count())
        self.spin_jobs.setValue(1)
        self.gridLayout.addWidget(self.spin_jobs, 2, 5, 1, 1)
        self.bt_auto_j = QtWidgets.QPushButton(Form)
        self.bt_auto_j.setObjectName("bt_auto_j")
        self.bt_auto_j.clicked.connect(self.auto_jobs)
        self.gridLayout.addWidget(self.bt_auto_j, 2, 6, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "百度图片爬虫"))
        self.label_key.setText(_translate("Form", "关键词"))
        self.bt_crawl.setText(_translate("Form", "爬取"))
        self.label_dir.setText(_translate("Form", "保存目录"))
        self.bt_select.setText(_translate("Form", "选择"))
        self.label_start.setText(_translate("Form", "起始"))
        self.label_max.setText(_translate("Form", "最大张数"))
        self.label_jobs.setText(_translate("Form", "线程数"))
        self.bt_auto_j.setText(_translate("Form", "自动选择"))
    def dowload_img(self,img_url,dirname,i):
        form=img_url.split('.')[-1]
        if not (form.lower() in ['jpg','png','gif']):
            form='png'
            print('Unknown format for img_url {u}\n Save as a PNG file')
        fname=os.path.join(dirname,str(i)+'.'+form)
        print('Download image {i} to file {fname}'.format(i=i,fname=fname))
        try:
            data=requests.get(img_url).content
            with open(fname,'wb') as f:
                f.write(data)
        except (requests.exceptions.BaseHTTPError,IOError):
            print(traceback.format_exc())
            print('Got error during download img \n{img}\n to file \n{fname}\nPass'.format(img=img_url,fname=fname))
            return 0
        else:
            return 1
    
    def select_dir(self):
        path=QFileDialog.getExistingDirectory(self,'选择保存路径',(self.dirname if self.dirname else './'))
        self.edit_dir.setText(path)
        
    def auto_jobs(self):
        self.spin_jobs.setValue(cpu_count())
            
    def crawl(self):
        self.dirname,self.word=self.edit_dir.text(),self.edit_key.text()
        if not self.dirname:
            print('请指定保存目录！')
            self.select_dir()
            if not self.word:
                print('请输入关键词！')
            return
        mkdir(self.dirname)
        self.max_num,self.start_page,self.nb_jobs=self.spin_max.value(),self.spin_start.value(),self.spin_jobs.value()
        if self.nb_jobs<2:
            print('正在使用单线程下载')
            nb_succeed=self.crawl_s()
        else:
            print('正在使用{}线程下载'.format(self.nb_jobs))
            nb_succeed=crawl_p(self.word,self.dirname,self.max_num,self.start_page,self.nb_jobs)
        print('爬取完毕！\n\n共成功爬取{s}/{e}张图片，保存到文件夹：{d}'.format(s=nb_succeed,e=self.max_num,d=self.dirname))
    def crawl_s(self):
        nb_succeed=0
        for i,img_url in enumerate(get_img_urls(self.word,self.max_num,self.start_page)):
            nb_succeed+=self.dowload_img(img_url,self.dirname,i)
        return nb_succeed

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        freeze_support()
    try:
        with open('./readme.txt','r',encoding='utf-8') as f:
            print(f.read())
    except:
        traceback.print_exc()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

