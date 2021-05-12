import asyncio

from pipelines.input_rig import InputRig

class TestInputRig:
	@classmethod
	async def fibonacci(cls, self, output_q:asyncio.Queue, fib_range:int=None):
		async def fib(fib_num):
			fib_prev = 1
			fib_prev_prev = 0
			for _ in range(fib_range):
				_cur = fib_prev + fib_prev_prev
				fib_prev_prev = fib_prev
				fib_prev = _cur
				yield _cur
				
		async for i in fib(fib_range):
			print(f':. putting val ~> {i}')
			await output_q.put(i)
			await asyncio.sleep(i%3)


async def q_consumer(q):
	while(True):
		print('q elt ~> ', await q.get())

async def main():
	output_dests =  [asyncio.Queue()]
	asyncio.create_task(q_consumer(output_dests[0]))
	_t = InputRig(name='test_input_rig',
				  coro=TestInputRig.fibonacci,
				  output_dests=output_dests,
				  fib_range= 10 )
	
	

if __name__ == '__main__':
	asyncio.get_event_loop().create_task(main())
	asyncio.get_event_loop().run_forever()
