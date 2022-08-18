import datetime
import time

import alarm


class Log:
    def __init__(self):
        data = datetime.datetime.now()
        self.nome = 'LOG-SiViA-' + str(data.strftime("%d-%m-%Y"))

    def loga(self, camera):
        with open(self.nome, 'a') as arquivo:
            arquivo.write(f'\n{time.asctime()} - ALARME - CAMERA {camera}')


if __name__ == '__main__':
    log = Log()
    log.loga(1)

    alarme = alarm.Alarm('55216845')
    alarme.toca_alarme()
