## plan of action
 This is a dummy workflow structure. I'll be using this to build the interface to the pipelines classes

There are two choices to make -
1.  Should this be like an rpc where the client specifies the pipelines ?
2.	Should the workflows be defined on the server and the client specifies which one to use ?

### The `Process` node - (InletQueue, Processor Coro, <foreign> OutletQueue)

```python

class Processor:
	def __init__(self, coro, maxsize):
		self.__inputQueue = asyncio.Queue(maxsize = maxsize)	
		self.__outputQueue = None
		self.__coro = coro

	@property
	def input_q(self):
		return self.__inputQueue

	def set_outQueue(self, q_out):
		"""
		q_out <foreign> __inputQueue of some other Processor
		"""
		self.__outputQueue = q_out

	async def _processor_task(self, q_in, q_out, coro, *args, **kwargs):
		try:
			while(True):

				get element from q_in
				result = await coro(q_in)
				put result in q_out
				
		except asyncio.CancelledError:
			...
		except Exception as e:
			...
	
```
--------------

### The `ProcessorGroup` - Grouping Related coroutines in a class

```python

class ProcessorGroup(type): 	# most probably an abstract class
	"""
	Contains a group of functions that are treated as a node in the pipeline.
	Each 
	node     := ( InletQueue, Processor, OutletQueue ) and, 
	pipeline := ( node1 -> node2 -> node3 )
	"""

```

```python

class Workflow1Funcs(ProcessorGroup):
	"""
	The coros should be static methods as they should not have a state.
	If they need to maintain a state, they should use the pipeline object
	that they are associated with
	"""

	@staticmethod
	async def method1( q_elem, *args, **kwargs) -> 'pipeline_processor':
		print('method1 called')
		pass

	@staticmethod
	async def method2(self, q_elem, *args, **kwargs) -> 'pipeline_processor':
		print('method2 called')
		pass
	
	@staticmethod
	async def method1(self, q_elem, *args, **kwargs) -> 'pipeline_processor':
		print('method2 called')
		pass
```

------------

### The `Pipeline` Creator - Creating Pipelines using `client` input and a `ProcessorGroup` subclass


