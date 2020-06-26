from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from user_airsearch import * # 航班查询
from user_ordersearch import * # 订单查询
from user_ticketprint import * # 机票打印
from user_ticketunsubscribe import * # 机票退订
from user_airstatus import * # 航班预订情况
import sys, pymysql

class select_window(QMainWindow):
	'''
	服务选择界面
	'''
	def __init__(self):
		super().__init__()
		self.date = '2020年5月19日'
		self.initUI()
		self.connectdb()
		
	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		self.setGeometry(300,300,800,600)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('北京大兴国际机场机票预订管理系统-用户端')

		# 左侧大兴机场图片
		pic1 = QPixmap('background.jpeg')
		self.lb1 = QLabel(self)
		self.lb1.setGeometry(0,0,640,600)
		self.lb1.setScaledContents(True)
		self.lb1.setPixmap(pic1)

		# 右侧大兴机场标志
		pic2 = QPixmap('title.png')
		self.lb2 = QLabel(self)
		self.lb2.setGeometry(670,20,100,45)
		self.lb2.setScaledContents(True)
		self.lb2.setPixmap(pic2)

		# 日期
		self.lb3 = QLabel(self)
		self.lb3.setGeometry(660,80,120,30)
		self.lb3.setText(self.date)
		self.lb3.setAlignment(Qt.AlignCenter)

		# 数据库连接状态
		self.lb4 = QLabel(self)
		self.lb4.setGeometry(660,120,120,30)
		self.lb4.setText('数据库未连接')
		self.lb4.setAlignment(Qt.AlignCenter)

		self.bt1 = QPushButton('航班查询',self)
		self.bt2 = QPushButton('订单查询',self)
		self.bt3 = QPushButton('机票打印',self)
		self.bt4 = QPushButton('机票退订',self)
		self.bt5 = QPushButton('航班预订情况',self)
		self.bt6 = QPushButton('连接数据库',self)
		self.bt7 = QPushButton('退出',self)

		self.bt1.move(670,170)
		self.bt2.move(670,230)
		self.bt3.move(670,290)
		self.bt4.move(670,350)
		self.bt5.move(670,410)
		self.bt6.move(670,470)
		self.bt7.move(670,530)

		self.bt1.clicked.connect(self.AirSearch)
		self.bt2.clicked.connect(self.OrderSearch)
		self.bt3.clicked.connect(self.TicketPrint)
		self.bt4.clicked.connect(self.TicketUnsubscribe)
		self.bt5.clicked.connect(self.AirStatus)
		self.bt6.clicked.connect(self.connectdb)
		self.bt7.clicked.connect(qApp.quit)

	def check(self):
		'''
		检查数据库是否连接
		'''
		if self.bt6.isEnabled():
			return False
		else:
			return True

	def alert(self):
		'''
		连接数据库提醒
		'''
		QMessageBox.information(self,'提示','请先连接数据库！',QMessageBox.Ok)

	def AirSearch(self):
		'''
		航班查询
		'''
		if self.check():
			self.hide()
			self.airs = AirSearch()
			self.airs.show()
		else:
			self.alert()

	def OrderSearch(self):
		'''
		订单查询
		'''
		if self.check():
			self.hide()
			self.uo = user_ordersearch()
			self.uo.show()
		else:
			self.alert()

	def TicketPrint(self):
		'''
		机票打印
		'''
		if self.check():
			self.hide()
			self.tp = user_ticketprint()
			self.tp.show()
		else:
			self.alert()

	def TicketUnsubscribe(self):
		'''
		机票退订
		'''
		if self.check():
			self.hide()
			self.utu = user_ticket_unsubscribe()
			self.utu.show()
		else:
			self.alert()

	def AirStatus(self):
		'''
		航班预订情况
		'''
		
		if self.check():
			self.hide()
			self.astatus = user_airstatus()
			self.astatus.show()
		else:
			self.alert()
		

	def connectdb(self):
		'''
		连接数据库，选择界面的连接仅为后续作测试用，连接后关闭即可
		'''
		try:
			self.airinfo = pymysql.connect(user='root',passwd='123456',db='airinfo',charset='utf8',\
					unix_socket='/var/run/mysqld/mysqld.sock')
			self.lb4.setText('数据库已连接')
			self.bt6.setEnabled(False)

			self.airinfo.close() 
		except:
			pass
