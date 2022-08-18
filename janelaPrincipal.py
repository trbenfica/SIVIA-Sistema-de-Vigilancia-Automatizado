from PyQt5 import uic
from PyQt5.QtCore import QTime, QThread, QObject
from PyQt5.QtWidgets import *
from configparser import ConfigParser, NoSectionError
import config as cfg
from dark import DarkDetection


class Worker(QObject):

    def __init__(self, hora_inicial: QTime, hora_final: QTime, arquivo, sonoro, sms):
        super().__init__()
        self.nome_arquivo = arquivo
        self.hora_ini = hora_inicial
        self.hora_final = hora_final
        self.sonoro = sonoro
        self.sms = sms

    def run(self):
        hora_atual = QTime.currentTime()
        if self.hora_ini < hora_atual < self.hora_final:
            detection = DarkDetection(self.nome_arquivo, self.sonoro, self.sms)
            detection.detect()


class JanelaSiViA(QMainWindow):
    def __init__(self):
        super(JanelaSiViA, self).__init__()

        self.detection = None
        self.thread_detection = QThread()
        self.hora_final_cam = ['', '', '', '']
        self.le_arquivo_cam = ['', '', '', '']
        self.hora_inicial_cam = ['', '', '', '']

        #   Carrega arquivo .ui
        uic.loadUi("SiViA.ui", self)

        #   #    Definição de Widgets    #    #
        #   Tab geral das câmeras
        self.tab_geral: QTabWidget = self.findChild(QTabWidget, "cams")

        #   Tabs das câmeras
        self.tab_cam1: QWidget = self.tab_geral.findChild(QWidget, "cam1")
        self.tab_cam2: QWidget = self.tab_geral.findChild(QWidget, "cam2")
        self.tab_cam3: QWidget = self.tab_geral.findChild(QWidget, "cam3")
        self.tab_cam4: QWidget = self.tab_geral.findChild(QWidget, "cam4")

        #   Botões propriedades das câmeras
        self.pb_cam1: QPushButton = self.findChild(QPushButton, "pushButton_cam1")
        self.pb_cam2: QPushButton = self.findChild(QPushButton, "pushButton_cam2")
        self.pb_cam3: QPushButton = self.findChild(QPushButton, "pushButton_cam3")
        self.pb_cam4: QPushButton = self.findChild(QPushButton, "pushButton_cam4")

        #   Botões procurar arquivo de vídeo
        self.pb_arquivo_cam1: QPushButton = self.tab_cam1.findChild(QPushButton, "pushButton_procurarCam1")
        self.pb_arquivo_cam2: QPushButton = self.tab_cam2.findChild(QPushButton, "pushButton_procurarCam2")
        self.pb_arquivo_cam3: QPushButton = self.tab_cam3.findChild(QPushButton, "pushButton_procurarCam3")
        self.pb_arquivo_cam4: QPushButton = self.tab_cam4.findChild(QPushButton, "pushButton_procurarCam4")

        #   LineEdit caminhos arquivos
        self.le_arquivo_cam[0]: QLineEdit = self.tab_cam1.findChild(QLineEdit, "lineEdit_caminhoCam1")
        self.le_arquivo_cam[1]: QLineEdit = self.tab_cam2.findChild(QLineEdit, "lineEdit_caminhoCam2")
        self.le_arquivo_cam[2]: QLineEdit = self.tab_cam3.findChild(QLineEdit, "lineEdit_caminhoCam3")
        self.le_arquivo_cam[3]: QLineEdit = self.tab_cam4.findChild(QLineEdit, "lineEdit_caminhoCam4")

        #   TimeEdits hora inicial
        self.hora_inicial_cam[0]: QTimeEdit = self.tab_cam1.findChild(QTimeEdit, "timeEdit_inicialCam1")
        self.hora_inicial_cam[1]: QTimeEdit = self.tab_cam2.findChild(QTimeEdit, "timeEdit_inicialCam2")
        self.hora_inicial_cam[2]: QTimeEdit = self.tab_cam3.findChild(QTimeEdit, "timeEdit_inicialCam3")
        self.hora_inicial_cam[3]: QTimeEdit = self.tab_cam4.findChild(QTimeEdit, "timeEdit_inicialCam4")

        #   TimeEdits hora final
        self.hora_final_cam[0]: QTimeEdit = self.tab_cam1.findChild(QTimeEdit, "timeEdit_finalCam1")
        self.hora_final_cam[1]: QTimeEdit = self.tab_cam2.findChild(QTimeEdit, "timeEdit_finalCam2")
        self.hora_final_cam[2]: QTimeEdit = self.tab_cam3.findChild(QTimeEdit, "timeEdit_finalCam3")
        self.hora_final_cam[3]: QTimeEdit = self.tab_cam4.findChild(QTimeEdit, "timeEdit_finalCam4")

        #   Botões de configuração
        self.pb_procurar: QPushButton = self.findChild(QPushButton, "pushButton_procurar")
        self.pb_salvar: QPushButton = self.findChild(QPushButton, "pushButton_salvar")
        self.pb_cancelar: QPushButton = self.findChild(QPushButton, "pushButton_cancelar")

        #   LineEdits de configuração
        self.caminho_log: QLineEdit = self.findChild(QLineEdit, "lineEdit_caminho")
        self.telefone_alerta: QLineEdit = self.findChild(QLineEdit, "lineEdit_telefone")

        #   CheckBox de alerta
        self.alerta_sonoro: QCheckBox = self.findChild(QCheckBox, "checkBox_sonoro")
        self.alerta_telefone: QCheckBox = self.findChild(QCheckBox, "checkBox_telefone")

        #   #   Conectar o click    #    #
        #   Botões de propriedades
        self.pb_cam1.clicked.connect(lambda: self.tab_geral.setCurrentIndex(0))
        self.pb_cam2.clicked.connect(lambda: self.tab_geral.setCurrentIndex(1))
        self.pb_cam3.clicked.connect(lambda: self.tab_geral.setCurrentIndex(2))
        self.pb_cam4.clicked.connect(lambda: self.tab_geral.setCurrentIndex(3))

        #   Botão de procurar caminho do arquivo de log
        self.pb_procurar.clicked.connect(self.procura_log)

        #   Botões de procurar caminho dos arquivos
        self.pb_arquivo_cam1.clicked.connect(lambda: self.procura_arquivo(0))
        self.pb_arquivo_cam2.clicked.connect(lambda: self.procura_arquivo(1))
        self.pb_arquivo_cam3.clicked.connect(lambda: self.procura_arquivo(2))
        self.pb_arquivo_cam4.clicked.connect(lambda: self.procura_arquivo(3))

        #   Botões de salvar e descartar alterações
        self.pb_salvar.clicked.connect(self.salvar_alteracoes)
        self.pb_cancelar.clicked.connect(self.descartar_alteracoes)

        #   Configuração
        self.ultima_config = ConfigParser()
        self.inicia_config()

        #   Habilita visualização da janela
        self.centralizar()
        self.show()

    def centralizar(self):
        """Centraliza a janela na tela."""
        resolucao = QDesktopWidget().screenGeometry()
        self.move((resolucao.width() / 2) - (self.frameSize().width() / 2),
                  (resolucao.height() / 2) - (self.frameSize().height() / 2))

    def procura_log(self):
        """Abre o QFileDialog para seleção da pasta."""
        caminho = QFileDialog.getExistingDirectory(self)
        self.caminho_log.setText(str(caminho))

    def salvar_alteracoes(self):
        """Salva as alterações feitas."""

        self.ultima_config['GERAL'] = {
            'alerta_sonoro': str(self.alerta_sonoro.isChecked()),
            'alerta_sms': str(self.alerta_telefone.isChecked()),
            'telefone': str(self.telefone_alerta.text()),
            'log_path': self.caminho_log.text()
        }

        for x in range(0, 4):
            self.ultima_config['cam' + str(x + 1)] = {
                'hora_inicial': str(self.hora_inicial_cam[x].time().toString()),
                'hora_final': str(self.hora_final_cam[x].time().toString()),
                'file_path': str(self.le_arquivo_cam[x].text())
            }

        # criação de uma thread para que não ocorra o travamento da interface gráfica
        self.detection = Worker(self.hora_inicial_cam[0].time(), self.hora_final_cam[0].time(), self.le_arquivo_cam[0].text(), self.alerta_sonoro.isChecked(), self.alerta_telefone.isChecked())
        self.detection.moveToThread(self.thread_detection)
        self.thread_detection.started.connect(self.detection.run)
        self.thread_detection.start()

        cfg.salvar_config(self.ultima_config)

    def imprimir_config(self):
        """Salva as alterações feitas."""
        print(f'Configurações\n'
              f'\tAlerta sonoro: {self.alerta_sonoro.isChecked()}\n'
              f'\tAlerta telefone: {self.alerta_telefone.isChecked()}\n'
              f'\ttelefone: {self.telefone_alerta.text()}\n'
              f'\tLog: {self.caminho_log.text()}')
        for x in range(0, 4):
            print(f'Cam{x+1}\n'
                  f'\tHora Ini: {self.hora_inicial_cam[x].time().toString()}\n'
                  f'\tHora Final: {self.hora_final_cam[x].time().toString()}\n'
                  f'\tArquivo de vídeo: {self.le_arquivo_cam[x].text()}')

    def descartar_alteracoes(self):
        config = self.ultima_config
        self.alerta_sonoro.setChecked(config.getboolean('GERAL', 'alerta_sonoro'))
        self.alerta_telefone.setChecked(config.getboolean('GERAL', 'alerta_sms'))
        self.telefone_alerta.setText(config['GERAL']['telefone'])
        self.caminho_log.setText(config['GERAL']['log_path'])
        for x in range(0, 4):
            cam_atual = config['cam' + str(x + 1)]
            self.hora_inicial_cam[x].setTime(QTime.fromString(cam_atual['hora_inicial'], 'HH:mm:ss'))
            self.hora_final_cam[x].setTime(QTime.fromString(cam_atual['hora_final'], 'HH:mm:ss'))
            self.le_arquivo_cam[x].setText(cam_atual['file_path'])

    def inicia_config(self):
        try:
            self.ultima_config.read('config.ini')
            self.descartar_alteracoes()
        except NoSectionError:
            erro = QMessageBox()
            erro.setText('Não foi encontrado arquivo de configuração!!!')
            erro.setWindowTitle('SiViA')
            erro.exec_()
            self.ultima_config = cfg.config_default()
            self.descartar_alteracoes()

    def procura_arquivo(self, cam):
        """Abre o QFileDialog para seleção do arquivo de vídeo."""
        caminho = QFileDialog.getOpenFileName(filter='Arquivo de Vídeo (*.mp4 *.mkv *.avi)')
        self.le_arquivo_cam[cam].setText(caminho[0])
