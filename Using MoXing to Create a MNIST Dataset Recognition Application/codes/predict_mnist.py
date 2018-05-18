import numpy as np
import predict_pb2
import prediction_service_pb2

from PIL import Image
from grpc.beta import implementations
from tensorflow.contrib.util import make_tensor_proto


IMAGE_PATH = '/export1/zzy/mnist/3.png'    #����ʵ�ʴ�Ԥ��ͼƬ�ı����ַ�޸Ĳ���
HOST = '10.155.167.202'  #����ʵ�ʷ���IP��ַ�޸�
PORT = 31670             #����ʵ�ʷ���˿ں��޸�
MODEL_NAME = 'mnist'     #����ʵ�ʷ������в���model_name�޸�
SIGNATURE_NAME = 'predict_object'
MAX_RESPONSE_TIME = 3000

image = Image.open(IMAGE_PATH)
image = image.resize((28, 28), Image.ANTIALIAS)
image = image.convert('L')
image = np.asarray(image, dtype=np.float32)
image = np.reshape(image, (1, 28 * 28))

channel = implementations.insecure_channel(HOST, PORT)
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

request = predict_pb2.PredictRequest()
request.model_spec.name = MODEL_NAME
request.model_spec.signature_name = SIGNATURE_NAME
request.inputs['images'].CopyFrom(make_tensor_proto(image, shape=list(image.shape)))

response = stub.Predict(request, MAX_RESPONSE_TIME)
prediction = response.outputs['predictions']
print(prediction)