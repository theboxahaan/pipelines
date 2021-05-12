from .processor import Processor
import traceback
import logging

class InputRig(Processor):
	
	async def _input_handler(self, input_src:list=None):
		return None
	
	async def _processor(self, *args, **kwargs):
		try:
			logging.info('%s starting processor ...', repr(self))
			_temp = await self._processor_coro(self, self._output_queue, *args, **kwargs)
		
		except Exception as e:
			logging.error('[processor]\n%s', traceback.format_exc())
			
class OutputRig(Processor):
	
	async def _output_handler(self, input_src:list=None):
		return None
	
#	async def _processor(self, *args, **kwargs):
#		try:
#			logging.info('%s starting processor ...', repr(self))
#			_temp = await self._processor_coro(self, self._output_queue, *args, **kwargs)
#		
#		except Exception as e:
#			logging.error('[processor]\n%s', traceback.format_exc())
