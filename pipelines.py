import asyncio
import uuid

loop = asyncio.get_event_loop()

class Pipeline:
	pass


class getAnnotated(type):
	def __new__(cls, name, bases, namespace):
		# print(namespace)
		class_obj = type.__new__(cls, name, bases, dict(namespace))
		class_obj.processing_coroutine_list = [k for k,v in namespace.items() if (v.__annotations__ if hasattr(v, '__annotations__') else {}).get('return', False) == 'process' ]
		return class_obj

class Processor(metaclass=getAnnotated):
	"""
	Represents a Queue-Consumer pair
	"""
	def __init__(self, maxsize = 2, name=None, *args, **kwargs):
		self.__uuid = uuid.uuid4()
		self.__queue = asyncio.Queue(maxsize = maxsize)
		print(self.processing_coroutine_list)
		# self._consumer_task_spawner = asyncio.create_task(self._consumer_task(*args, **kwargs), name='spawn')
		self.__consumer_task_list = [asyncio.create_task(self._consumer_task(getattr(self, i), *args, **kwargs), name=i) for i in self.processing_coroutine_list]
		

	def __repr__(self):
		return f"<Processor: UUID:{self.__uuid}>"

	def get_uuid(self):
		return self.__uuid

	async def push_q(self, elt):
		await self.__queue.put(elt)

	async def _consumer_task(self, coro, *args, **kwargs):
		try:
			print(":. Consumer Task Started...")
			while(True):
				_elt = await self.__queue.get()
				await coro(_elt, *args, **kwargs) 
				self.__queue.task_done()
		except asyncio.CancelledError:
			print(f":.{repr(self)} ~> cancelled()")
		except Exception as e:
			raise e
	
	async def process(q_elt, *args, **kwargs):
		raise NotImplementedError

	async def close_processor(self):
		await self.__consumer_task.cancel()



if __name__ == '__main__':
	async def main():

		class Reverse(Processor):
			async def reverse(self, q_elt:str ) -> 'process' :
				print(q_elt[::-1])
			
			# async def toascii(self, q_elt:str ) -> 'process' :
			# 	print(list(bytes(q_elt.encode('utf-8'))))

		temp = Reverse(maxsize=2, name=None)
		print(repr(temp))
		await temp.push_q('ahaan')
		print('pushed to q..')
		await temp.push_q('dabholkar')

	asyncio.run(main())	
