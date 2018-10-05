from keras import backend as K

def free_mem():
    K.clear_session()
    K.get_session().close()
    cfg = K.tf.ConfigProto()
    cfg.gpu_options.allow_growth = True
    K.set_session(K.tf.Session(config=cfg))
    K.clear_session()

free_mem()
