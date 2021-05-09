import uuid
import asyncio
import logging


#TODO add logging to module	


class Processor:
	"""
	Class Processor represents a node in the processing pipeline where
	node := (input Q, processor, output Q, accumulator)
	pipeline := node1 ->  node2 -> node3
	"""

	def __init__(self, input_queue:asyncio.Queue = None, output_queue:asyncio.Queue =None, coro=None, *args, **kwargs):
		self.__input_queue = asyncio.Queue() if input_queue is None else input_queue
		self.__output_queue = asyncio.Queue() if output_queue is None else output_queue
		self.__processor_coro = coro
		self.__uuid = uuid.uuid4()
		self.__output_accumulator = []

		self.__input_handler_task = asyncio.create_task(self.__input_handler(), name=self.__uuid + self.__input_hanlder.__qualname__)
		self.__processor_task = asyncio.create_task(self._processor(*args, **kwargs), name=self.__uuid + self.__processor_coro.__qualname__)

	async def __input_handler(self):
		"""
		Helper Function to handle multiple input sources and populate 
		the input_queue of each Processor object. 
		The only constraint is that the number of inputs coming in from each 
		input source are equal in number, otherwise the processor Q's will be kept
		waiting...
		.
		"""



	async def _processor(self, *args, **kwargs):
		try:
			while(True):
				_temp = await self.__input_queue.get()
				_temp = await self.__processor_coro(self, _temp, *args, **kwargs)
				if self.__output_queue is None:
					self.__output_accumulator.append(_temp)
				else:
					await self.__output_queue.put(_temp)

		except asyncio.CancelledError:
			pass
		except Exception as e:
			raise
	
	@property
	def input_queue(self):
		return self.__input_queue
	
	@property.setter
	def output_queue(self, out_q:asyncio.Queue):
		self.output_queue = out_q
