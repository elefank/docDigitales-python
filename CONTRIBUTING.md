# Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto DocDigitales Python Client! Este documento proporciona las pautas y el proceso para contribuir.

## Proceso de Desarrollo

1. **Crear una rama**
   - Las ramas deben crearse desde `develop`
   - Nomenclatura de ramas: `feature/nombre-caracteristica` o `fix/nombre-correccion`
   - Ejemplo: `feature/agregar-validacion-rfc` o `fix/correccion-error-autenticacion`

2. **Desarrollo**
   - Sigue las convenciones de código de Python (PEP 8)
   - Escribe pruebas unitarias para nuevo código
   - Mantén la cobertura de pruebas por encima del 80%
   - Documenta el código usando docstrings

3. **Commit**
   - Usa mensajes de commit descriptivos
   - Formato: `tipo(alcance): descripción`
   - Ejemplos:
     - `feat(auth): implementa validación de token`
     - `fix(client): corrige manejo de errores en facturación`
     - `docs(readme): actualiza instrucciones de instalación`

4. **Pull Request**
   - Crea un PR hacia la rama `develop`
   - Incluye una descripción clara de los cambios
   - Asegúrate de que todos los tests pasen
   - Solicita revisión de al menos un mantenedor

## Estándares de Código

1. **Python**
   - Python 3.10 o superior
   - Sigue PEP 8
   - Usa type hints
   - Documenta con docstrings (formato Google)

2. **Tests**
   - Usa pytest
   - Mantén la cobertura de código alta
   - Incluye casos de prueba positivos y negativos

3. **Documentación**
   - Actualiza README.md si es necesario
   - Documenta cambios en la API
   - Incluye ejemplos de uso

## Proceso de Revisión

1. **Revisión de Código**
   - Todos los PRs requieren al menos una aprobación
   - Los revisores verificarán:
     - Calidad del código
     - Cobertura de pruebas
     - Documentación
     - Cumplimiento de estándares

2. **CI/CD**
   - Los PRs deben pasar todas las pruebas
   - No debe haber conflictos
   - Debe cumplir con los estándares de linting

## Estructura de Ramas

- `main`: Código en producción
- `develop`: Rama de desarrollo principal
- `feature/*`: Nuevas características
- `fix/*`: Correcciones de bugs
- `release/*`: Preparación de releases

## Versiones

Seguimos [Semantic Versioning](https://semver.org/):
- MAJOR: Cambios incompatibles con versiones anteriores
- MINOR: Nuevas funcionalidades compatibles
- PATCH: Correcciones de bugs compatibles

## Contacto

Si tienes dudas o necesitas ayuda:
- Abre un issue en GitHub
- Contacta a los mantenedores del proyecto 