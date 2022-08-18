from darkflow.net.build import *
import cv2
import os
from alarm import Alarm
from log import Log

# Recebe o diretório atual
cwd = os.getcwd()

# Tempo inicial, para o cálculo do tempo empregado para o processamento do vídeo
tempo_ini = time.time()


class DarkDetection:
	def __init__(self, entrada_video, sonoro, sms):
		self.tempo = 0.0
		self.vezes_detectado = 0
		self.alarme = Alarm('+5553999315490', sonoro, sms)
		self.log = Log()
		self.entrada_video = entrada_video
		# Configuração e inicialização da rede
		options = {"model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.3}
		self.rede = TFNet(options)

		# Carregando o arquivo de vídeo
		self.video = cv2.VideoCapture(self.entrada_video)

		# Obtendo a quantidade de frames no vídeo
		self.qtd_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

	def detect(self):
		i = 0
		while i < self.qtd_frames:
			# Carrega um frame do vídeo
			retorno, frame = self.video.read()
			if not retorno:
				break

			# Passa pela rede
			result = self.rede.return_predict(frame)

			conf = 0
			for item in result:
				if item.get('label') == 'person':
					conf = item.get('confidence')
					break
			if conf != 0:
				self.pessoa()
				# print(f'FRAME {i + 1} - person \t{conf}')
			# else:
			print(f'FRAME {i + 1} - nada')
			i += 1

		self.video.release()

	def pessoa(self):
		# print('DETECTOU')
		self.vezes_detectado += 1
		if time.time() - self.tempo > 15 and self.vezes_detectado > 2:
			self.vezes_detectado = 0
			self.log.loga(1)
			self.tempo = time.time()
			self.alarme.toca_alarme()


if __name__ == '__main__':
	dark = DarkDetection('test_videos/quarto10.mp4')
	dark.detect()


