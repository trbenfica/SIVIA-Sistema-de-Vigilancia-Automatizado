import time
from configparser import ConfigParser


def config_default() -> ConfigParser:
    """Cria arquivo de configuração com os valores vazios."""
    novo = ConfigParser()

    novo['GERAL'] = {
        'alerta_sonoro': 'false',
        'alerta_sms': 'false',
        'telefone': '',
        'log_path': ''
    }

    for x in range(1, 5):
        novo['cam' + str(x)] = {
            'hora_inicial': '00:00:00',
            'hora_final': '00:00:00',
            'file_path': ''
        }
    return novo


def print_config(arquivo: ConfigParser):
    """Print todo arquivo de configuração."""
    for section in arquivo.sections():
        print(section)
        for item in arquivo.items(section):
            print('\t' + item[0] + " = " + arquivo.get(section, item[0]))


def salvar_config(arquivo: ConfigParser) -> bool:
    """Recebe as configurações a serem salvas e retorna true caso sucesso e false caso contrário."""
    try:
        with open('config.ini', 'w') as novo_arquivo:
            arquivo.write(novo_arquivo)
    except (PermissionError, FileExistsError) as e:
        return False
    return True


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    salvar_config(config)
    config['GERAL']['alerta_sonoro'] = 'true'
    print(config.getboolean('GERAL', 'alerta_sonoro'))
    print_config(config)
    with open('log.txt', 'a', ) as file:
        file.write(f'\n{time.asctime()} - ALARME - CAMERA {str(4)}')

