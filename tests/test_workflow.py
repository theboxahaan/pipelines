import asyncio
from pipelines.processor import Processor
import uuid

class ProcessorGroup(type):
	pass

class StringFunc(ProcessorGroup):
	
	@classmethod
	async def input_str(cls, self, q_out, num:int=None):
		acc = []
		for _ in range(num):
			acc.append(str(uuid.uuid4()))
		
		for i in acc:
			await q_out.put(i)
			await asyncio.sleep(acc.index(i) % 4)
	
	@classmethod
	async def output_str(cls, self, q_elt):
		print('output_str: ', q_elt)

	@classmethod
	async def reverse(cls, self, q_elt:tuple):
		# print(f':. inside classmethod {q_elt}~> {q_elt[::-1]}')
		return q_elt[0][::-1]
	
	@classmethod
	async def append_reverse(cls, self, q_elt:tuple):
		q_elt_1, q_elt_2  = q_elt 
		# print(f':. inside classmethod {q_elt_1} + {q_elt_2} ~> {q_elt_1[::-1] + q_elt_2[::-1]}')
		return q_elt_1[::-1] + q_elt_2[::-1]
	
	@classmethod
	async def toupper(cls, self, q_elt:tuple):
		q_elt, = q_elt
		return q_elt.upper()
	
	@classmethod
	async def tolower(cls, self, q_elt:tuple):
		q_elt,q_elt_2 = q_elt
		return q_elt.lower()


async def test_rig():
	
	input_src = [asyncio.Queue(), asyncio.Queue(), asyncio.Queue()]
	output_dest = [asyncio.Queue()]
	print(':. creating test Processor object')
	async def dummy_consumer():
		try:
			while(True):
				_elt = await output_dest[0].get()
				print(":. [dummy_consumer]", _elt)
		except asyncio.CancelledError:
			pass
		except Exception as e:
			print(e)
			raise
	
	asyncio.create_task(dummy_consumer())
	_t = Processor(coro = StringFunc.reverse, input_srcs=input_src[:1], output_dests=output_dest)
	_m = Processor(coro = StringFunc.append_reverse, input_srcs = input_src[1:], output_dests=output_dest)
	for _ in range(1):
		await input_src[0].put('ahaan')
		await asyncio.sleep(1)

	print(_m)
	await input_src[1].put('dabholkar')
	await input_src[2].put('dabholkar')
	print(':. finishd coro')
	# start output_dest consumer task that prints items to stdout


if __name__ == '__main__':
	asyncio.get_event_loop().create_task(test_rig())
	asyncio.get_event_loop().run_forever()
