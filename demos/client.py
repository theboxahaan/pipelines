import asyncio
import random
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
	print(':. established connection to server')
	await send_msg_for_process()


@sio.event
async def send_msg_for_process():

	_temp = [hex(random.getrandbits(128)) for _ in range(5)]
	print(f':. Random strings generated ~> {_temp}')

	input_d = \
	{
		'nodes': {
			'inp'  : {'coro': 'ProcessFunc.inputcoro', 'args': {'strings_from_client': _temp}},
			'coro1': {'coro': 'ProcessFunc.coro1'},
			'coro2': {'coro': 'ProcessFunc.coro2'},
			'coro3': {'coro': 'ProcessFunc.coro3'},
			'out'  : {'coro': 'ProcessFunc.outputcoro', 'properties': {'aggregate_inputs': False}},
		},
		'graph': {
			'inp'  : ('coro1', ),
			'coro1': ('coro2', 'coro3'),
			'coro2': ('out', ),
			'coro3': ('out', ),
			'out'  : None,
		},	
	}

	await sio.emit('process_msg', input_d)


@sio.event
async def recv(data):
	print(f'Received data: {data}')

async def main():
	await sio.connect('http://localhost:8080')
	await sio.wait()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	try:
		loop.create_task(main())
		loop.run_forever()
	except Exception as e:
		print('caught excrption')
		loop.run_until_complete(sio.disconnect())
		loop.close()
	finally:
		print(":. client exiting...")
