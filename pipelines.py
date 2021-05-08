import asyncio
import uuid

loop = asyncio.get_event_loop()

class Pipeline:
	pass

class Processor:
	"""
	Represents a Queue-Consumer pair
	"""
	def __init__(self, maxsize = 2, name=None, *args, **kwargs):
		self.__uuid = uuid.uuid4()
		self.__queue = asyncio.Queue(maxsize = maxsize)
		self.__consumer_task = asyncio.create_task(self._consumer_task(*args, **kwargs), name=name)
		

	def __repr__(self):
		return f"<Processor: UUID:{self.__uuid}>"

	def get_uuid(self):
		return self.__uuid

	async def push_q(self, elt):
		await self.__queue.put(elt)

	async def _consumer_task(self, *args, **kwargs):
		try:
			print(":. Consumer Task Started...")
			while(True):
				_elt = await self.__queue.get()
				await self.process(_elt, *args, **kwargs) 
				self.__queue.task_done()
		except asyncio.CancelledError:
			print(f":.{repr(self)} ~> Task cancelled")
		except Exception as e:
			raise e
	
	async def process(q_elt, *args, **kwargs):
		raise NotImplementedError

	async def close_processor(self):
		await self.__consumer_task.cancel()



if __name__ == '__main__':
	async def main():

		class Reverse(Processor):
			async def process(self, q_elt:str):
				print(q_elt[::-1])

		temp = Reverse(maxsize=2, name=None)
		print(repr(temp))
		await temp.push_q('ahaan')
		print('pushed to q..')

	asyncio.run(main())	
