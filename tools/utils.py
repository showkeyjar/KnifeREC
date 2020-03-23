import configparser as cfp

"""
公共方法
"""
conf = None


def read_config(conf_path='config.ini'):
    global conf
    if conf is None:
        conf = cfp.ConfigParser()
        conf.read(conf_path, encoding='utf-8')
    return conf


def guess_config_value(v):
    ret = None
    if v == 'True':
        ret = True
    elif v == 'False':
        ret = False
    if ret is None:
        ret = v
    return ret


def read_flask_config():
    global conf
    if conf is None:
        conf = read_config()
    flask_conf = conf._sections['flask']
    if flask_conf is not None:
        flask_conf = {str(k).upper(): guess_config_value(v) for k, v in flask_conf.items()}
    return flask_conf
