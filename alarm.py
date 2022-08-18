import pygame
from twilio.rest import Client


class Alarm:
    def __init__(self, numberPhone, sonoro, sms):
        self.numero = numberPhone
        self.sonoro = sonoro
        self.sms = sms

    def toca_alarme(self):
        pygame.init()
        pygame.mixer.music.load('alarm-5s.mp3')
        pygame.mixer.music.set_volume(.05)
        if self.sonoro:
            pygame.mixer.music.play(loops=3)
        account_sid = 'ACc4c5362a2123042930c99372fa1a825e'
        auth_token = 'b2c37e46780afa73a26521320dfb4e94'
        client = Client(account_sid, auth_token)
        if self.sms:
            client.messages.create(from_='+18457139103', to=self.numberPhone,
                       body='ALERTA!!!! Sua casa pode estar sob invasão, por favor verifique as áreas cadastradas')

