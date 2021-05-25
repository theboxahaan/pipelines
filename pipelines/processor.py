import uuid
import asyncio
import logging
import traceback

class Processor:
	"""
	Class Processor represents a node in the processing pipeline where
	node := (input Q, processor, output Q, accumulator)
	pipeline := node1 ->  node2 -> node3

	"""

	def __init__(self, 
				 name:str = None,
				 input_queue:asyncio.Queue=None, 
				 output_queue:asyncio.Queue=None, 
				 coro=None, 
				 input_srcs:list=None, 
				 output_dests:list=None, 
				 env_vars:dict=None,
				 *args, **kwargs):

		self._input_queue        = asyncio.Queue() if input_queue is None else input_queue
		self._output_queue       = asyncio.Queue() if output_queue is None else output_queue
		self._processor_coro     = coro
		self._uuid               = str(uuid.uuid4())
		self._name               = str(name)
		self._output_accumulator = []
		self._input_srcs         = input_srcs
		self._output_dests       = output_dests
		self.env_vars            = env_vars

		self._input_handler_task = asyncio.create_task(self._input_handler(self._input_srcs))

		self._processor_task = asyncio.create_task(self._processor(*args, **kwargs))

		self._output_handler_task = asyncio.create_task(self._output_handler(self._output_dests))

		logging.info('instantiated %s', str(self))

	async def _input_handler(self, input_src:list=None):
		"""
		Helper Function to handle multiple input sources and populate 
		the input_queue of each Processor object. 
		The only constraint is that the number of inputs coming in from each 
		input source are equal in number, otherwise the processor Q's will be kept
		waiting...
		.
		"""
		try:
			logging.info('%s started input handler...', repr(self))
			while(True):

				# acquire a single input elt from each of the source
				# (liason q's)
				cur_input = []
				if input_src is None or len(input_src) == 0:
					logging.error('input sources cannot be None or empty list ... exiting input_handler')
					raise asyncio.CancelledError
				for _src in input_src:
					cur_input.append(await _src.get())
				
				# put the acquired input inside the Processor's input_queue
				await self._input_queue.put(tuple(cur_input))

		except asyncio.CancelledError:
			logging.warning('%s input_handler cancelled', str(self))
		except Exception as e:
			logging.error('[input_handler]\n%s', traceback.format_exc())
			raise 

	async def _output_handler(self, output_dest:list=None):
		"""
		Helper Function to handle multiple output destinations and populate 
		the output_queue of each Processor object. 
		"""
		try:
			logging.info('%s started output handler...', repr(self))
			while(True):

				if output_dest is None or len(output_dest) == 0:
					logging.error('output dests cannot be None or empty list... exiting output_handler')
					raise asyncio.CancelledError

				# acquire a single output elt from the output queue
				cur_output = await self._output_queue.get()
				
				# put the acquired output into the dest(liason) q's
				for _dest in output_dest:
					await _dest.put(cur_output)
					
		except asyncio.CancelledError:
			logging.warning('%s output_handler cancelled', str(self))
		except Exception as e:
			logging.error('[output_handler]\n%s', traceback.format_exc())
			raise 


	async def _processor(self, *args, **kwargs):
		try:
			logging.info('%s started processor ...', repr(self))
			while(True):
				_temp = await self._input_queue.get()
				async def _processor_task(_temp, *Aargs, **Akwargs):
					logging.info('starting processor task...')
					try:
						_temp = await self._processor_coro(self, _temp, *Aargs, **Akwargs)
						if self._output_queue is None:
							self._output_accumulator.append(_temp)
						else:
							await self._output_queue.put(_temp)
					
					except Exception as e:
						logging.error('[processor_task]\n%s', traceback.format_exc())

				asyncio.create_task(_processor_task( _temp, *args, **kwargs))

		except asyncio.CancelledError:
			logging.warning('%s processor cancelled', str(self))
		except Exception as e:
			logging.error('[processor]\n%s', traceback.format_exc())
			raise 
	
	@property
	def input_queue(self) -> asyncio.Queue:
		return self._input_queue
	
	@property
	def output_queue(self) -> asyncio.Queue:
		return self._output_queue
	
	@property
	def uuid(self) -> str:
		return self._uuid

	@property
	def name(self) -> str:
		return self._name

	@property
	def liason_queues(self) -> tuple:
		return (self._input_srcs, self._output_dests)

	@property
	def processor_coro(self):
		return self._processor_coro
	
	def __repr__(self) -> str:
		return f"<Processor:{self._uuid}, coro:{self._processor_coro.__qualname__}>"
	
	def __str__(self) -> str:
		return f"<Processor:{self._uuid};{self._name}>"
	


class InputProcessor(Processor):
	
	async def _processor(self, *args, **kwargs):
		try:
			logging.info('%s starting IO processor ...', repr(self))
			await self._processor_coro(self, self._output_queue, *args, **kwargs)
		
		except Exception as e:
			logging.error('[processor]\n%s', traceback.format_exc())
			
