# This module contains a test class that groups related coroutines for a particular
# workflow.
class ProcessorGroup(type):
	pass


class CoroGroup1(ProcessorGroup):
	
	@classmethod
	async def method1(cls, self, q_elt, *args, **kwargs):
		print(f':. in method 1...of Processor object <{self}, {id(self)}>')

	@classmethod
	async def method2(cls, self, q_elt, *args, **kwargs):
		print(f':. in method 2...of Processor object <{self}, {id(self)}>')



