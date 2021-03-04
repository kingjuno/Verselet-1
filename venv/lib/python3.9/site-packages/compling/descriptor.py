import inspect
import typing
from typing import get_type_hints
from inspect import getcallargs

def __get_class_that_defined_method__(meth):
    """Returns the class that defined method"""

    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
           if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing

    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls

    return getattr(meth, '__objclass__', None)  # handle special descriptor objects

def invokesuper(func):
    """method descriptor: invokes the super method."""

    def onCall(*args, **kwargs):
        _ = getattr(__get_class_that_defined_method__(func).__bases__[0], func.__name__)(*args, **kwargs)
        return func(*args, **kwargs)

    onCall.__name__ = func.__name__
    return onCall

def paramtypecheck(func):
    """method descriptor: check the parameter types."""

    def onCall(*args, **kwargs):
        hints = get_type_hints(func)

        call_args = getcallargs(func, *args, **kwargs)
        is_method = inspect.ismethod(func)

        # param index
        for param, paramtype in hints.items():
            if param == 'self' and is_method or param == 'return':
                continue

            # check if param is Iterable[str]
            if paramtype == typing.Iterable[str]:
                if not all([isinstance(s, str) for s in call_args[param]]):
                    raise TypeError("{} must be Iterable[str]".format(param))
                else:
                    continue

            # check if param is optional
            is_optional = not type(paramtype) == type
            paramtype = [paramtype] if not is_optional else paramtype.__args__

            if not is_optional:
                paramtypename = paramtype[0].__name__
            else:
                paramtypename = 'typing.Union[{}]'.format(", ".join(p.__name__ for p in paramtype))

            # Type Error
            if not type(call_args[param]) in paramtype:
                raise TypeError("{} must be {}, not {}".format(param, paramtypename,
                                                               type(call_args[param]).__name__))

        return func(*args, **kwargs)

    onCall.__name__ = func.__name__
    return onCall

def paramtypechecktarget(params):
    """method descriptor: check the parameter types."""

    def paramtypecheckt(func):
        """method descriptor: check the parameter types."""

        def onCall(*args, **kwargs):
            hints = get_type_hints(func)

            call_args = getcallargs(func, *args, **kwargs)
            is_method = inspect.ismethod(func)

            # param index
            for param, paramtype in hints.items():
                if param not in params:
                    continue

                # check if param is Iterable[str]
                if paramtype == typing.Iterable[str]:
                    if not all([isinstance(s, str) for s in call_args[param]]):
                        raise TypeError("{} must be Iterable[str]".format(param))
                    else:
                        continue

                # check if param is optional
                is_optional = not type(paramtype) == type
                paramtype = [paramtype] if not is_optional else paramtype.__args__

                if not is_optional:
                    paramtypename = paramtype[0].__name__
                else:
                    paramtypename = 'typing.Union[{}]'.format(", ".join(p.__name__ for p in paramtype))

                # Type Error
                if not type(call_args[param]) in paramtype:
                    raise TypeError("{} must be {}, not {}".format(param, paramtypename,
                                                                   type(call_args[param]).__name__))

            return func(*args, **kwargs)

        onCall.__name__ = func.__name__
        return onCall

    return paramtypecheckt

def f2att(function):
    """On first call, it stores the result of the method in an attribute. <br/>
       On next ones, the result will be returned without executing the method."""
    def onCall(self, *args):
        attribute = function.__name__ + '_'
        if not hasattr(self, attribute):
            self.__dict__[attribute] = function(self, *args)
        return self.__dict__[attribute]

    return onCall