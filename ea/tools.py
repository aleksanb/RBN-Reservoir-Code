class Mixin(object):
    def __init__(self, name, fn, kwargs={}):
        self.__call__ = fn
        self.name = name
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __repr__(self):
        arguments = ', '.join(['%s=%s' % (key, self.kwargs[key])
                               for key in self.kwargs])
        return self.name + ('(%s)' % arguments if arguments else '')
