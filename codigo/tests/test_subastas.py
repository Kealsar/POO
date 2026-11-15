"""Pruebas con biblioteca estándar: python -m unittest discover -s tests -v."""
import unittest
from decimal import Decimal
from modelos import Comprador, ErrorSubasta, EstadoSubasta, Vendedor
from sistema import SistemaSubastas


class TestSubastas(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaSubastas()
        self.vendedor = Vendedor(1, "Ana", "ana@ejemplo.com")
        self.comprador = Comprador(2, "Luis", "luis@ejemplo.com")
        self.sistema.registrar_usuario(self.vendedor)
        self.sistema.registrar_usuario(self.comprador)
        self.producto = self.vendedor.crear_producto(10, "Libro", "Edición usada")
        self.subasta = self.sistema.publicar_subasta(20, self.producto, "15.00")

    def test_puja_valida_y_ganador(self):
        puja = self.comprador.ofertar(self.subasta, "20.00")
        self.assertEqual(puja.importe, Decimal("20.00"))
        self.assertIs(self.subasta.cerrar(), self.comprador)
        self.assertEqual(self.subasta.estado, EstadoSubasta.CERRADA)

    def test_no_permite_precio_igual_o_menor(self):
        for importe in ("15.00", "10.00"):
            with self.subTest(importe=importe), self.assertRaises(ErrorSubasta):
                self.comprador.ofertar(self.subasta, importe)

    def test_rechaza_vendedor(self):
        impostor = Comprador(1, "Ana", "ana@ejemplo.com")
        with self.assertRaises(ErrorSubasta):
            impostor.ofertar(self.subasta, "16.00")

    def test_no_permite_puja_despues_del_cierre(self):
        self.subasta.cerrar()
        with self.assertRaises(ErrorSubasta):
            self.comprador.ofertar(self.subasta, "16.00")

    def test_cierre_sin_ofertas(self):
        self.assertIsNone(self.subasta.cerrar())
        self.assertEqual(self.subasta.precio_actual, Decimal("15.00"))

    def test_no_permita_doble_cierre(self):
        self.subasta.cerrar()
        with self.assertRaises(ErrorSubasta):
            self.subasta.cerrar()

    def test_importes_invalidos(self):
        for importe in ("abc", "16.001", "NaN", "Infinity"):
            with self.subTest(importe=importe), self.assertRaises(ErrorSubasta):
                self.comprador.ofertar(self.subasta, importe)

    def test_usuario_duplicado(self):
        with self.assertRaises(ErrorSubasta):
            self.sistema.registrar_usuario(Comprador(2, "Otro", "otro@ejemplo.com"))

    def test_producto_duplicado_en_subasta(self):
        with self.assertRaises(ErrorSubasta):
            self.sistema.publicar_subasta(21, self.producto, "30.00")

    def test_lista_pujas_no_modificable_externamente(self):
        self.assertIsInstance(self.subasta.pujas, tuple)


if __name__ == "__main__":
    unittest.main()
