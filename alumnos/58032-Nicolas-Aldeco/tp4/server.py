import asyncio as asy
import time
from argparse import ArgumentParser
from server_tools import ServerTools
st = None


# Atiendo las conexiones al servidor:
async def handler(reader, writer):
    ip, port = writer.get_extra_info('peername')
    asy.create_task(logs(ip, port))

    lec = await reader.read(st.get_size())
    listGet = st.parseGet(lec)

    req = ''
    for p, elem in enumerate(listGet[0].split(' ')):
        if p == 1:
            req = elem

    if req == '/' or req == '/index':
        req = '/index.html'

    resolve = st.fileLookUp(req)
    # Escribo cabecera, y si hay un error tambien el html de este.
    writer.write(resolve[1])
    # Si la peticion fue correcta, envio el archivo.
    if resolve[0] == 200:
        with open(st.get_root()+req, 'rb') as file:
            while True:
                lec = file.read(st.get_size())
                if not lec:
                    break
                writer.write(lec)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


# Armo un log:
async def logs(ip, port):
    now = time.ctime()
    log = f'> client: {ip}:{port}; date:{now}\n'
    with open('logs.txt', 'a') as logs:
        logs.write(log)
 

async def main():
    server = await asy.start_server(
        handler, st.get_ip(), st.get_port()
    )
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    arg = ArgumentParser(
        description='Servidor asincronico de multimedias',
        usage='server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura] -i [direccion ip]'
    )
    arg.add_argument(
        '-r', '--root', nargs=1, type=str,
        help='ruta de los archivos', default=['/root'], metavar=''
    )
    arg.add_argument(
        '-p', '--port', nargs=1, type=int,
        help='puerto para el servidor', default=[8080], metavar=''
    )
    arg.add_argument(
        '-s', '--size', type=int, help='bloque de lectura',
        default=[255], metavar=''
    )
    arg.add_argument(
        '-i', '--ip', type=str, help='direccion ip',
        default=['localhost'], metavar=''
    )

    argms = arg.parse_args()
    dicc = {
        'root': argms.root[0],
        'port': argms.port[0],
        'size': argms.size[0],
        'ip': argms.ip[0]
    }
    # Creo una instancia del obj ServerTools con herramientas
    st = ServerTools(dicc)
    # Creo un index.html con los archivos que esten en el directorio root
    st.listDirInIndex()
    asy.run(main())
