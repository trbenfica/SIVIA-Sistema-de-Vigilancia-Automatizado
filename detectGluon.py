import gluoncv as gluon
import cv2
import mxnet
import time
import os
# Recebe o diretório atual
cwd = os.getcwd()

# Tempo inicial, para o cálculo do tempo empregrado para o processamento do vídeo
tempo_ini = time.time()

# Carregamento do modelo
net = gluon.model_zoo.get_model('ssd_512_mobilenet1.0_voc', pretrained=True)

# Carregando o arquivo de vídeo
arquivo = 'test_videos/intruder2j.mp4'
cap = cv2.VideoCapture(os.path.join(cwd, arquivo))

# Obtendo a quantidade de frames no vídeo
NUM_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
i = 0
while i < NUM_FRAMES:
    # Carrega um frame do vídeo
    ret, frame = cap.read()
    if not ret:
        break

    # Faz o pré processamento da imagem
    frame = mxnet.nd.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).astype('uint8')
    rgb_nd, scaled_frame = gluon.data.transforms.presets.ssd.transform_test(frame, short=512, max_size=700)

    # Roda a imagem na rede de reconhecimento
    classes, confi, caixas = net(rgb_nd)

    # Verifica se alguma pessoa foi reconhecida no frame
    trust = 0
    confi_aux = confi.asnumpy()
    classes_aux = classes.asnumpy()
    for x in range(100):
        if confi_aux[0][x][0] >= 0.3:   # utilizando 30% de certeza
            if int(classes_aux[0][x][0]) == 14:
                trust = confi_aux[0][x][0] * 100

    # Printa se foi reconhecida alguma pessoa
    if trust > 0:
        print(f'Frame {i+1} - pessoa \t{trust:.2f}')
    else:
        print(f'Frame {i+1} - nada')

    # Mostra o resultado com as caixas de identificação
    escala = 1.0 * frame.shape[0] / scaled_frame.shape[0]
    saida = gluon.utils.viz.cv_plot_bbox(frame.asnumpy(), caixas[0], confi[0], classes[0], class_names=net.classes,
                                         scale=escala)
    gluon.utils.viz.cv_plot_image(saida)
    cv2.waitKey(1)
    i += 1

cap.release()
cv2.destroyAllWindows()
print(f'Arquivo: {arquivo}')
print(f'Número de frames: {NUM_FRAMES}')
print('TEMPO(s): ' + str(time.time() - tempo_ini))

