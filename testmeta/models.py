from django.db import models

def subclassed_model():
    """
    Decorator maker function.
    Adds property to recover subclass model instance.
    :return: class with subclass property
    """
    def decorator(cls):
        print("decorator received", cls)

        def subclass_instance(self):
            self_class_name = type(self).__name__
            if hasattr(self, '_subclass_instance'):
                #print("_subclass_instance already configured:", self._subclass_instance)
                return self._subclass_instance
            else:
                last_n = None
                for n in dir(self):
                    if n in ['subclass_instance', 'virtual_instance']:
                        continue
                    val = getattr(self, n, None)
                    class_name = type(val).__name__
                    if isinstance(val, cls):
                        #print('  ¿Descendiente?')
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
            if self.__class__.__subclasses__():
                #print("  sub: ", self.__class__.__subclasses__())
                #print("  virtual: ", self.subclass_instance.virtual_instance)
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

@subclassed_model()
class Hija(MadreAbstracta):
    pass

class Nieta(Hija):
    apodito = models.CharField(max_length=10)

class Nieto(Hija):
    renombrado = models.CharField(max_length=10)
