"""Demostración automática reproducible. Ejecutar: python main.py"""
from modelos import Comprador, ErrorSubasta, Vendedor
from sistema import SistemaSubastas


def mostrar_rechazo(subasta, comprador, importe, etiqueta):
    try:
        comprador.ofertar(subasta, importe)
    except ErrorSubasta as exc:
        print(f"[RECHAZO ESPERADO] {etiqueta}: {exc}")
    else:
        raise AssertionError(f"La validación '{etiqueta}' debía rechazar la puja.")


def main() -> None:
    print("=== SISTEMA DE SUBASTAS ONLINE | SIMULACIÓN ===")
    sistema = SistemaSubastas()
    vendedor = Vendedor(1, "Ana Torres", "ana@ejemplo.com")
    comprador1 = Comprador(2, "Luis Pérez", "luis@ejemplo.com")
    comprador2 = Comprador(3, "María Ruiz", "maria@ejemplo.com")
    for usuario in (vendedor, comprador1, comprador2):
        sistema.registrar_usuario(usuario)
        print(f"Usuario registrado: {usuario.nombre} ({usuario.descripcion_rol()})")

    producto = vendedor.crear_producto(101, "Computadora portátil", "Equipo usado en buen estado")
    subasta = sistema.publicar_subasta(501, producto, "150.00")
    print(f"Subasta #{subasta.id}: {producto.nombre} | precio inicial: ${subasta.precio_inicial}")

    for comprador, importe in ((comprador1, "175.00"), (comprador2, "200.00"), (comprador1, "225.00")):
        puja = comprador.ofertar(subasta, importe)
        print(f"[PUJA ACEPTADA] {puja.comprador.nombre}: ${puja.importe}")

    mostrar_rechazo(subasta, comprador2, "220.00", "importe insuficiente")
    # Se demuestra el control incluso ante la tentativa de un vendedor con tipo Comprador.
    usuario_mismo_id = Comprador(vendedor.id, vendedor.nombre, vendedor.correo)
    mostrar_rechazo(subasta, usuario_mismo_id, "250.00", "vendedor intenta pujar")

    ganador = subasta.cerrar()
    print(f"Subasta cerrada | estado: {subasta.estado.value}")
    print(f"Ganador: {ganador.nombre if ganador else 'Sin ganador'} | precio final: ${subasta.precio_actual}")
    mostrar_rechazo(subasta, comprador2, "300.00", "subasta cerrada")
    assert len(subasta.pujas) == 3 and ganador is comprador1
    print("RESULTADO: demostración completada correctamente.")


if __name__ == "__main__":
    main()
