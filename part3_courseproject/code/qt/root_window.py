from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import login
import sys, pymysql, traceback

class Stream(QObject):
	'''
	将控制台的输出重定位到文本框
	'''
	newText = pyqtSignal(str)

	def write(self,text):
		self.newText.emit(str(text))

class root_window(QMainWindow):
	'''
	用户登录界面
	'''
	def __init__(self):
		super().__init__()
		self.initUI()
		sys.stdout = Stream(newText=self.onUpdateText)
		self.connectdb() # 自动连接数据库
	
	def onUpdateText(self,text):
		'''
		将控制台输出写到文本框中
		'''
		cursor = self.textbox.textCursor()
		cursor.movePosition(QTextCursor.End)
		cursor.insertText(text)
		self.textbox.setTextCursor(cursor)
		self.textbox.ensureCursorVisible()

	def closeEvent(self,event):
		'''
		将输出控制恢复默认
		'''
		sys.stdout = sys.__stdout__
		super().closeEvent(event)
	
	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",14))
		self.setGeometry(300,300,1000,600)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('北京大兴国际机场机票预订管理系统-管理员端')

		# 退出
		self.exit_action = QAction('退出',self)
		self.exit_action.setShortcut('Ctrl+Q')
		self.exit_action.triggered.connect(qApp.quit)

		# 注销
		self.logout_action = QAction('注销',self)
		self.logout_action.setShortcut('Ctrl+L')
		self.logout_action.triggered.connect(self.logout)

		# 关于系统
		self.sys_action = QAction('关于系统',self)
		self.sys_action.triggered.connect(self.about_sys)

		# 关于作者
		self.author_action = QAction('关于作者',self)
		self.author_action.triggered.connect(self.about_author)

		# 菜单栏
		self.menubar = self.menuBar()

		self.order_menu = self.menubar.addMenu('选项')
		self.order_menu.addAction(self.logout_action)
		self.order_menu.addAction(self.exit_action)

		self.about_menu = self.menubar.addMenu('关于')
		self.about_menu.addAction(self.sys_action)
		self.about_menu.addAction(self.author_action)

		# 文本输出框
		self.textbox = QTextEdit(self,readOnly=True)
		self.textbox.move(25,40)
		self.textbox.ensureCursorVisible()
		self.textbox.setLineWrapColumnOrWidth(1000)
		self.textbox.setLineWrapMode(QTextEdit.FixedPixelWidth)
		self.textbox.setFixedWidth(950)
		self.textbox.setFixedHeight(450)
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.textbox)

		# 文本输入框
		self.textinput = QTextEdit(self)
		self.textinput.setGeometry(25,500,725,75)

		# 数据库连接状态
		self.dbstatus = QLabel(self)
		self.dbstatus.setGeometry(775,500,200,25)
		self.dbstatus.setText('数据库未连接')
		self.dbstatus.setAlignment(Qt.AlignCenter)

		# 数据库连接按钮
		self.dbbt = QPushButton('连接',self)
		self.dbbt.setGeometry(775,550,75,25)
		self.dbbt.setShortcut('Ctrl+C')
		self.dbbt.clicked.connect(self.connectdb)

		# 执行按钮
		self.bt = QPushButton('执行',self)
		self.bt.setGeometry(900,550,75,25)
		self.bt.setShortcut('Ctrl+D')
		self.bt.clicked.connect(self.process)

		self.show()

	def connectdb(self):
		'''
		数据库连接模块
		'''
		try:
			if self.dbstatus.text()[-3] == '未':
				self.airinfo = pymysql.connect(user='root',passwd='123456',db='airinfo',charset='utf8',\
					unix_socket='/var/run/mysqld/mysqld.sock')
				self.dbstatus.setText('数据库已连接')
				print('Connecting to DATABASE airinfo successfully!\n')
				self.dbbt.setEnabled(False)
		except:
			print('Failed to connect to DATABASE airinfo!\n')

	def process(self):
		'''
		执行输出模块
		'''
		try:
			if self.dbstatus.text()[-3] == '未':
				print('The database is not in connection now!\n')
			else:
				sql = self.textinput.toPlainText().strip()
				print('>>> ' + sql)
				if sql != 'exit;':
					cursor = self.airinfo.cursor()
					cursor.execute(sql[:-1])
					data = cursor.fetchall()
					for i in data:
						print(i)
					print('\n')
					self.textinput.clear()
					cursor.close()
				else:
					self.textinput.clear()
					self.airinfo.close()
					self.dbstatus.setText('数据库未连接')
					self.dbbt.setEnabled(True)
					print('Goodbye.\n')
		except:
			self.textinput.clear()
			print(traceback.format_exc())

	def logout(self):
		'''
		注销
		'''
		self.hide()
		self.login = login.login() # 避免循环引用问题，必须import login而不是from ...
		self.login.show()

	def about_sys(self):
		'''
		关于系统
		'''
		QMessageBox.about(self,'关于系统','北京大兴国际机场机票预订管理系统\nVersion 1.0')

	def about_author(self):
		'''
		关于作者
		'''
		QMessageBox.about(self,'关于作者','作者: 王英嘉\n\
						学校: 华中科技大学\n\
						Email: yingjiawang@hust.edu.cn\n\
						Github: https://github.com/yingjia-git')
