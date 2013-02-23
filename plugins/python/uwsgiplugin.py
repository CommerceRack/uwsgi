import os,sys

from distutils import sysconfig

NAME='python'
GCC_LIST = ['python_plugin', 'pyutils', 'pyloader', 'wsgi_handlers', 'wsgi_headers', 'wsgi_subhandler', 'web3_subhandler', 'pump_subhandler', 'gil', 'uwsgi_pymodule', 'profiler', 'symimporter', 'tracebacker']

CFLAGS = ['-I' + sysconfig.get_python_inc(), '-I' + sysconfig.get_python_inc(plat_specific=True) ] 

if 'pypy_version_info' in sys.__dict__:
    CFLAGS.append('-DUWSGI_PYPY')

LDFLAGS = []

if not 'UWSGI_PYTHON_NOLIB' in os.environ:
    LIBS = sysconfig.get_config_var('LIBS').split() + sysconfig.get_config_var('SYSLIBS').split()
    if not sysconfig.get_config_var('Py_ENABLE_SHARED'):
        print(sysconfig.get_config_var('srcdir'))
        print(sysconfig.get_config_var('LIBPL'))
        print(sysconfig.get_config_var('LDLIBRARY'))
        print(sysconfig.get_config_var('LIBRARY'))
        print(os.listdir(sysconfig.get_config_var('LIBPL')))
        print(sysconfig.get_config_var('LDLIBRARY'))
        LIBS.append('%s/%s' % (sysconfig.get_config_var('LIBPL'), sysconfig.get_config_var('LIBRARY')))
    else:
        try:
            LDFLAGS.append("-L%s" % sysconfig.get_config_var('LIBDIR'))
            os.environ['LD_RUN_PATH'] = "%s" % (sysconfig.get_config_var('LIBDIR'))
        except:
            LDFLAGS.append("-L%s/lib" % sysconfig.PREFIX)
            os.environ['LD_RUN_PATH'] = "%s/lib" % sysconfig.PREFIX


        version = sysconfig.get_config_var('VERSION')
        try:
            version = version + sys.abiflags
        except:
            pass
        LIBS.append('-lpython' + version)
else:
    LIBS = []
