"""Servicio coordinador: registro de usuarios y publicación de subastas."""
from modelos import ErrorSubasta, Producto, Subasta, Usuario, Vendedor


class SistemaSubastas:
    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._subastas: dict[int, Subasta] = {}

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.id in self._usuarios:
            raise ErrorSubasta("Ya existe un usuario con ese identificador.")
        self._usuarios[usuario.id] = usuario

    def publicar_subasta(self, identificador: int, producto: Producto, precio_inicial: object) -> Subasta:
        if identificador in self._subastas:
            raise ErrorSubasta("Ya existe una subasta con ese identificador.")
        vendedor = self._usuarios.get(producto.vendedor.id)
        if not isinstance(vendedor, Vendedor) or vendedor is not producto.vendedor:
            raise ErrorSubasta("El vendedor debe estar registrado en el sistema.")
        if any(s.producto.id == producto.id for s in self._subastas.values()):
            raise ErrorSubasta("El producto ya cuenta con una subasta.")
        subasta = Subasta(identificador, producto, precio_inicial)
        self._subastas[identificador] = subasta
        return subasta

    def obtener_subasta(self, identificador: int) -> Subasta:
        try:
            return self._subastas[identificador]
        except KeyError as exc:
            raise ErrorSubasta("La subasta solicitada no existe.") from exc

    @property
    def usuarios(self) -> tuple[Usuario, ...]:
        return tuple(self._usuarios.values())

    @property
    def subastas(self) -> tuple[Subasta, ...]:
        return tuple(self._subastas.values())
