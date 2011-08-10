import warnings

warnings.warn('Please use elephantblog.views.legacy.views instead of elephantblog.views',
    DeprecationWarning)

from elephantblog.views.legacy.views import *
