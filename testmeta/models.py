from django.db import models

def subclassed_model():
    """
    Decorator maker function.
    Adds property to recover subclass model instance.
    If it received parameters, the decorator can make use of them
    because they are kept in the closure.
    :return: class with subclass property
    """
    def decorator(cls):
        print("decorator received", cls)

        def subclass_instance(self):
            if hasattr(self, '_subclass_instance'):
                #print("_subclass_instance already configured:", self._subclass_instance)
                return self._subclass_instance
            else:
                self_class_name = self.__class__.__name__
                for n in dir(self):
                    if n in ['subclass_instance', 'virtual_instance']:
                        continue
                    val = getattr(self, n, None)
                    class_name = val.__class__.__name__
                    if self_class_name != class_name \
                        and isinstance(val, self.__class__):
                        #print('  ¿Descendiente?', isinstance(val, self.__class__))
                        #print('    ', n)
                        #print('    Clase:   ', type(self), self_class_name)
                        #print('    Atributo:', type(val), class_name)
                        last_n = n
                        self._subclass_instance = val
                        return val
                self._subclass_instance = None
                return None
        prop = property(fget=subclass_instance)
        setattr(cls, 'subclass_instance', prop)


        def virtual_instance(self):
            #print("---")
            #print("[virtual_instance] ", type(self))
            if self.__class__.__subclasses__() and self.subclass_instance:
                #print("  name:", self.__class__.__name__)
                #print("  sub: ", self.__class__.__subclasses__())
                #print("  virtual: ", self.subclass_instance)
                return self.subclass_instance.virtual_instance
            else:
                #print("  no tiene sub")
                return self
        prop = property(fget=virtual_instance)
        setattr(cls, 'virtual_instance', prop)


        return cls
    return decorator


# Create your models here.
@subclassed_model()
class Abuela(models.Model):
    texto = models.CharField(max_length=10)

class MadreAbstracta(Abuela):
    class Meta:
        abstract = True

    def nombre(self):
        return "MA"


class Hija(MadreAbstracta):
    pass

class Nieta(Hija):
    apodito = models.CharField(max_length=10)

class Nieto(Hija):
    renombrado = models.CharField(max_length=10)
