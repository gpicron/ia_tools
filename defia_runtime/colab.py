import os

import humanize
import psutil
import tensorflow as tf
from keras import backend as K

tpu_address = None

try:
    import GPUtil as GPU

    GPUs = GPU.getGPUs()
    gpu = GPUs[0]
    device = '/gpu:0'
    tf.device(device)


    def __printm():
        process = psutil.Process(os.getpid())
        print("Gen RAM Free: " + humanize.naturalsize(psutil.virtual_memory().available),
              " I Proc size: " + humanize.naturalsize(process.memory_info().rss))
        print('GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB'.format(gpu.memoryFree,
                                                                                                    gpu.memoryUsed,
                                                                                                    gpu.memoryUtil * 100,
                                                                                                    gpu.memoryTotal))
except:

    if 'COLAB_TPU_ADDR' in os.environ:
        tpu_address = 'grpc://' + os.environ['COLAB_TPU_ADDR']

        print('TPU address is', tpu_address)

        print('TPU runtime detected')


    def __printm():
        process = psutil.Process(os.getpid())
        print("Gen RAM Free: " + humanize.naturalsize(psutil.virtual_memory().available),
              " I Proc size: " + humanize.naturalsize(process.memory_info().rss))
        print('No GPU')

__printm()


def print_memory_usage():
    """
    Print the current host memory usage and GPU memory usage
    """
    __printm()


def free_mem():
    """
    Free the GPU memory and reset Keras
    """
    K.clear_session()
    K.get_session().close()
    cfg = K.tf.ConfigProto()
    cfg.gpu_options.allow_growth = True
    K.set_session(K.tf.Session(config=cfg))
    K.clear_session()


free_mem()
