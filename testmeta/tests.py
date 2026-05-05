from django.test import TestCase
from testmeta.models import Abuela, MadreAbstracta, Hija, Nieta, Nieto


class NietaTestCase(TestCase):
    def setUp(self):
        self.nieta = Nieta.objects.create(texto="Nieta 1", apodito="Chibi")

    def test_recupera_nieta(self):
        """Debo poder recuperar a la nieta a partir de la abuela"""
        abuela = Abuela.objects.all()[0]
        print()
        print(abuela)
        print(dir(abuela))
        print('hija: ', abuela.hija)
        print('nieta: ', abuela.hija.nieta)
        self.assertEqual(abuela.hija.nieta, self.nieta)


        hija = Hija.objects.all()[0]
        print()
        print(hija)
        print(dir(hija))
        print('nombre: ', hija.nombre())
        print('abuela_ptr: ', hija.abuela_ptr)
        print('abuela_ptr_id: ', hija.abuela_ptr_id)
        print('hija:', hija.hija)
        print('nieta:', hija.nieta, hija.nieta.apodito)


        nieta = Nieta.objects.all()[0]
        print()
        print(nieta)
        print(dir(nieta))
        print('nombre: ', nieta.nombre())
        print('abuela_ptr: ', nieta.abuela_ptr)
        print('abuela_ptr_id: ', nieta.abuela_ptr_id)
        print('hija:', nieta.hija)
        print('nieta:', nieta.nieta, nieta.nieta.apodito)

        self.assertEqual(nieta.apodito, 'Chibi')
        self.assertEqual(nieta, nieta.nieta)
        self.assertEqual(nieta.abuela_ptr, abuela)
        self.assertNotEqual(nieta, abuela)
        self.assertIsInstance(nieta, type(abuela))
        self.assertIsInstance(nieta, abuela.__class__)





class NietoTestCase(TestCase):
    def setUp(self):
        self.nieto = Nieto.objects.create(texto="Nieto 1", renombrado="Kun")

    def test_recupera_nieto(self):
        """Debo poder recuperar al nieto a partir de la abuela,
        no confundir con la nieta"""
        abuela = Abuela.objects.all()[0]
        print()
        print(abuela)
        print(dir(abuela))
        print('hija: ', abuela.hija)
        print('nieto: ', abuela.hija.nieto)
        try:
            print('nieta: ', abuela.hija.nieta)
        except Hija.nieta.RelatedObjectDoesNotExist:
            print('Se dió cuenta de que no es nieta')

        self.assertEqual(abuela.hija.nieto, self.nieto)




class SubclassTestCase(TestCase):
    def setUp(self):
        # No se deben crear instancias de la clase extendible
        self.abuela = Abuela.objects.create(texto="Abuela")
        self.hija = Hija.objects.create(texto="Hija")
        self.nieta = Nieta.objects.create(texto="Nieta 1", apodito="Chibi")
        self.nieto = Nieto.objects.create(texto="Nieto 1", renombrado="Kun")

    def test_subclassed_model(self):
        print()
        print("""^_^ test_subclassed_model ^_^""")
        def print_info(instances, class_name):
            print(':) ', class_name)
            for i, instance in enumerate(instances):
                print(i, '.')
                print(" instancia:", instance)
                if hasattr(instance, 'subclass_instance'):
                    subclass_instance = instance.subclass_instance
                    print(" subclass_instance:     ", subclass_instance)
                    print(" subclass_instance_type:", type(instance.subclass_instance).__name__)
                else:
                    print(" no tiene subclass_instance")
                self.assertIsInstance(instance, type(instance))

        print_info(Abuela.objects.all(), 'Abuela')
        print_info(Hija.objects.all(), 'Hija')
        print_info(Nieta.objects.all(), 'Nieta')
        print_info(Nieto.objects.all(), 'Nieto')

    def test_virtual_instance(self):
        print()
        print("""^_^ test_virtual_instance ^_^""")
        for i, instance in enumerate(Abuela.objects.all()):
            if hasattr(instance, 'virtual_instance'):
                print(i, instance, instance.virtual_instance)
            else:
                print(i, instance)
