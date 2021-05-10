import asyncio
from processor import Processor

class ProcessorGroup(type):
	pass


async def test_rig():
	
	class ReverseFunc(ProcessorGroup):
		@classmethod
		async def reverse(cls, self, q_elt:tuple):
			q_elt,  = q_elt 
			# print(f':. inside classmethod {q_elt}~> {q_elt[::-1]}')
			return q_elt[::-1]
		
		@classmethod
		async def append_reverse(cls, self, q_elt:tuple):
			q_elt_1, q_elt_2  = q_elt 
			# print(f':. inside classmethod {q_elt_1} + {q_elt_2} ~> {q_elt_1[::-1] + q_elt_2[::-1]}')
			return q_elt_1[::-1] + q_elt_2[::-1]

	input_src = [asyncio.Queue(), asyncio.Queue(), asyncio.Queue()]
	output_dest = [asyncio.Queue()]
	print(':. creating test Processor object')
	_t = Processor(coro = ReverseFunc.reverse, input_srcs=input_src[:1], output_dests=output_dest)
	await input_src[0].put('ahaan')
	
	_m = Processor(coro = ReverseFunc.append_reverse, input_srcs = input_src[1:], output_dests=output_dest)
	await input_src[1].put('dabholkar')
	await input_src[2].put('dabholkar')

	# start output_dest consumer task that prints items to stdout

	async def dummy_consumer():
		try:
			while(True):
				print(":. [dummy_consumer]", await output_dest[0].get())
		except asyncio.CancelledError:
			pass
		except Exception as e:
			raise
	
	asyncio.create_task(dummy_consumer())

if __name__ == '__main__':
	asyncio.run(test_rig())
