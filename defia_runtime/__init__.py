import os

import humanize
import psutil
import tensorflow as tf

tpu_address = None

try:
    import GPUtil as GPU
    GPUs = GPU.getGPUs()
    # XXX: only one GPU on Colab and isn't guaranteed
    gpu = GPUs[0]
    device='/gpu:0'
    tf.device(device)

    def printm():
        process = psutil.Process(os.getpid())
        print("Gen RAM Free: " + humanize.naturalsize( psutil.virtual_memory().available ), " I Proc size: " + humanize.naturalsize( process.memory_info().rss))
        print('GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB'.format(gpu.memoryFree, gpu.memoryUsed, gpu.memoryUtil*100, gpu.memoryTotal))
except:

    if 'COLAB_TPU_ADDR' in os.environ:
        tpu_address = 'grpc://' + os.environ['COLAB_TPU_ADDR']

        print ('TPU address is', tpu_address)

        print ('TPU runtime detected')

    def printm():
        process = psutil.Process(os.getpid())
        print("Gen RAM Free: " + humanize.naturalsize( psutil.virtual_memory().available ), " I Proc size: " + humanize.naturalsize( process.memory_info().rss))
        print('No GPU')

printm()