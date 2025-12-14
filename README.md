# Rack Asset Tag Scanner

Script en Python para escanear asset tags de compute trays en un rack mediante SSH,
automatizando la obtención de información de inventario y evitando el escaneo manual.

## Qué hace
- Se conecta vía SSH a la RSCM del rack
- Consulta los asset tags de múltiples compute trays usando CLI
- Imprime los resultados en formato listo para copiar y pegar

## Uso
1. Definir las credenciales SSH como variables de entorno
2. Ejecutar el script
3. Ingresar la IP de la RSCM cuando se solicite

## Requisitos
- Python 3
- paramiko

## Notas
Este script está pensado para ejecutarse en entornos automatizados
(PXE / servidores sin interacción gráfica).
