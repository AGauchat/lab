#!/usr/bin/python3
import asyncio
import time
from argparse import ArgumentParser
import os
from respuesta import Respuesta

root = None
lista = ''

# Atiendo las conexiones al servidor:
async def handler(reader, writer):
    ip, port = writer.get_extra_info('peername')
    asyncio.create_task(logs(ip, port))

    lec = await reader.read(255)
    archivo = lec.decode().splitlines()[0].split()[1]


    if archivo == '/' or archivo == '/index':
        archivo = '/index.html'

    resolve = rta.verifArchivo(archivo)
    
    writer.write(resolve[1])
    
    if resolve[0] == 200:
        with open(os.getcwd() + args.root[0] + archivo, 'rb') as file:
            while True:
                lec = file.read(args.size[0])
                if not lec:
                    break
                writer.write(lec)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

def ListaArchivos(ldir, dir):
    global lista
    ldir.sort(key=lambda elem: elem.find('.') == -1)
    for elem in ldir:
        rDir = dir.replace(root, '')
        if elem.find('.') != -1:
            lista += f'\n<ul><a href=\'{rDir}/{elem}\'>{elem}</a></ul>'
        else:
            lista += f'<ul>\\{elem}'
            ListaArchivos(os.listdir(dir+'/'+elem), dir+'/'+elem)
    lista += '</ul>'
    return lista + '</ul>'

def GenerarIndex():
    lista = ListaArchivos(os.listdir(path=root), root)
    body = f'''
<!DOCTYPE html>
<html>
    <head>
        <title>My Web Server</title>        
    </head>
    <body>
        <h1>Servidor</h1>
        <h2>Archivos:</h2>
        <div>
            {lista}
        </div>
    </body>
</html>'''
    with open(root + '/index.html', 'w') as index:
        index.write(body)

# Armo un log:
async def logs(ip, port):
    now = time.ctime()
    log = f'> client: {ip}:{port}; date:{now}\n'
    with open('logs.txt', 'a') as logs:
        logs.write(log)
 

async def main(ip, port):
    server = await asyncio.start_server(
        handler, ip, port
    )
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    arg = ArgumentParser(description='Servidor asincronico de multimedias', usage='server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura] -i [direccion ip]')
    arg.add_argument('-r', '--root', nargs=1, type=str, help='ruta de los archivos', default=['/root'], metavar='')
    arg.add_argument('-p', '--port', nargs=1, type=int, help='puerto', default=[8080], metavar='')
    arg.add_argument('-s', '--size', type=int, help='bloque de lectura', default=[255], metavar='')
    arg.add_argument('-i', '--ip', type=str, help='direccion ip', default=['0.0.0.0'], metavar='')

    args = arg.parse_args()

    root = os.getcwd() + args.root[0]

    dicc = {
        'root': args.root[0],
        'port': args.port[0],
        'size': args.size[0],
        'ip': args.ip[0]
    }
    
    # Creo una instancia del obj ServerTools con herramientas
    rta = Respuesta(dicc)
    # Creo un index.html con los archivos que esten en el directorio root
    GenerarIndex()
    asyncio.run(main(args.ip[0], args.port[0]))