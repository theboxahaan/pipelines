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

	def __init__(self, 
				 input_queue:asyncio.Queue=None, 
				 output_queue:asyncio.Queue=None, 
				 coro=None, 
				 input_srcs=None, 
				 output_dests=None, 
				 *args, **kwargs):

		self.__input_queue = asyncio.Queue() if input_queue is None else input_queue
		self.__output_queue = asyncio.Queue() if output_queue is None else output_queue
		self.__processor_coro = coro
		self.__uuid = str(uuid.uuid4())
		self.__output_accumulator = []
		self.__input_srcs = input_srcs
		self.__output_dests= output_dests

		self.__input_handler_task = asyncio.create_task( 
			self.__input_handler(self.__input_srcs),
			name=self.__uuid + self.__input_handler.__qualname__)

		self.__processor_task = asyncio.create_task(
			self._processor(*args, **kwargs),
			name=self.__uuid + self.__processor_coro.__qualname__)

		self.__output_handler_task = asyncio.create_task(
			self.__output_handler(self.__output_dests),
			name=self.__uuid + self.__output_handler.__qualname__)

	async def __input_handler(self, input_src:list=None):
		"""
		Helper Function to handle multiple input sources and populate 
		the input_queue of each Processor object. 
		The only constraint is that the number of inputs coming in from each 
		input source are equal in number, otherwise the processor Q's will be kept
		waiting...
		.
		"""
		try:
			while(True):
				# acquire a single input elt from each of the sources
			
				cur_input = []
				if input_src is None:
					print(':. input sources cannot be None')
					raise asyncio.CancelledError
				for _src in input_src:
					cur_input.append(await _src.get())
				
				# put the acquired input inside the Processor's input_queue

				await self.__input_queue.put(tuple(cur_input))
		except asyncio.CancelledError:
			pass
		except Exception as e:
			raise 

	async def __output_handler(self, output_dest:list=None):
		"""
		Helper Function to handle multiple output destinations and populate 
		the output_queue of each Processor object. 
		"""
		try:
			while(True):
				# acquire a single outputelt from the output queue
			
				cur_output = await self.__output_queue.get()
				
				# put the acquired input inside the Processor's input_queue
				if output_dest is None or output_dest ==[]:
					print(f':. ouptut_handler ~> {cur_output}')
				else:
					for _dest in output_dest:
						await _dest.put(cur_output)
					
		except asyncio.CancelledError:
			pass
		except Exception as e:
			raise 


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
	
	# @property.setter
	# def output_queue(self, out_q:asyncio.Queue):
	# 	self.output_queue = out_q


async def test_rig():
	
	class ReverseFunc:
		@classmethod
		async def reverse(cls, self, q_elt:tuple):
			q_elt,  = q_elt 
			print(f':. inside classmethod {q_elt}~> {q_elt[::-1]}')
			return q_elt[::-1]
		
		@classmethod
		async def append_reverse(cls, self, q_elt:tuple):
			q_elt_1, q_elt_2  = q_elt 
			print(f':. inside classmethod {q_elt_1} + {q_elt_2} ~> {q_elt_1[::-1] + q_elt_2[::-1]}')
			return q_elt_1[::-1] + q_elt_2[::-1]

	input_src = [asyncio.Queue(), asyncio.Queue(), asyncio.Queue()]
	print(':. creating test Processor object')
	_t = Processor(coro = ReverseFunc.reverse, input_srcs=input_src[:1], output_dests=None)
	await input_src[0].put('ahaan')
	

	_m = Processor(coro = ReverseFunc.append_reverse, input_srcs = input_src[1:], output_dests=None)
	await input_src[1].put('dabholkar')
	await input_src[2].put('dabholkar')


if __name__ == '__main__':

	# setup testrig for Processor object
	# test rig needs to provide input_srcs, [output_dests], coro
	asyncio.run(test_rig())
