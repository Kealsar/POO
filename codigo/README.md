# Sistema de Subastas Online — POO en Python

Práctica académica sobre casos de uso, diagramas UML y programación orientada a objetos. Aplicación de consola sin dependencias externas ni base de datos. Todos los datos son simulados y permanecen solo en memoria.

## Requisitos
- Python 3.10 o superior (recomendado Python 3.12+).

## Ejecución
Desde la carpeta `codigo`:

```bash
python main.py
```

## Pruebas
```bash
python -m unittest discover -s tests -v
```

## Archivos
- `modelos.py`: clases Usuario, Comprador, Vendedor, Producto, Subasta y Puja; reglas de negocio.
- `sistema.py`: clase SistemaSubastas, registro y publicación.
- `main.py`: simulación automática con ofertas válidas e inválidas, cierre y ganador.
- `tests/test_subastas.py`: pruebas de comportamiento y validación.
- `../diagramas/`: diagramas UML editables en diagrams.net (draw.io).
- `../informe/`: informe académico en Word y PDF.

## Reglas de negocio
1. La subasta nace activa con un precio inicial mayor que cero.
2. Solo se aceptan pujas estrictamente superiores al precio actual.
3. El usuario con la identidad del vendedor no puede pujar.
4. No se puede pujar una vez cerrada la subasta.
5. Al cerrar, la última puja válida determina al ganador; sin pujas, no hay ganador.
6. Los importes se procesan con `Decimal` hasta dos decimales.

## Alcance
No existen pagos reales, login, interfaz web ni persistencia. El cierre es explícito y controlado por la demostración. El control de identidad está simulado por identificadores únicos (no constituye autenticación real).

## Subir a GitHub
Crear un repositorio vacío en GitHub. En la carpeta raíz del proyecto ejecutar:

```bash
git init
git add .
git commit -m "Implementa sistema academico de subastas POO"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Reemplazar `USUARIO` y `REPOSITORIO` por los datos propios. No se incluye ningún enlace inventado.
