from aiohttp import web
import asyncio
import socketio
from pipelines.processor import Processor
from pipelines.plumber import Plumber


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


class ProcessFunc:
	
	@classmethod
	async def inputcoro(cls, self:Processor, q_out:asyncio.Queue, strings_from_client:list):
		for i in strings_from_client:
			print(f':. input-ing into pipeline ~> {i}')	
			await q_out.put(i)
		

	@classmethod
	async def coro1(cls, self:Processor, q_elt:tuple):
		await asyncio.sleep(3)	# to emulate an IO bound process
		return q_elt[0][::-1]
	
	@classmethod
	async def coro2(cls, self:Processor, q_elt:tuple):
		await asyncio.sleep(2)	# to emulate an IO bound process
		return q_elt[0].upper()

	@classmethod
	async def coro3(cls, self:Processor, q_elt:tuple):
		await asyncio.sleep(1)	#	to simulate an IO bound process
		return q_elt[0] + '-' + q_elt[0][::-1]
	
	@classmethod
	async def outputcoro(cls, self:Processor, q_elt:tuple):
		await sio.emit('recv', data=q_elt[0], to=self.env_vars['sid'] )

def getcoro(name):
	class_name , fn_name = name.split('.')
	return getattr(globals()[class_name], fn_name)

@sio.event
def connect(sid, environ):
	print('Connected to : ', sid)


@sio.event
def process_msg(sid, input_d):
	
	Plumber(input_d, coro_map=getcoro, env_vars={'sid':sid})

if __name__ == '__main__':
	web.run_app(app)
