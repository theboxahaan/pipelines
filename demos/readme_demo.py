import asyncio
from pipelines.processor import Processor
from pipelines.plumber import Plumber
import uuid

loop = asyncio.get_event_loop()

class StringFuncs:
    @classmethod
    async def reverse(cls, self:Processor=None, q_elt:tuple=None):
        return q_elt[0][::-1]

    @classmethod
    async def input_coro(cls, self:Processor=None, output_q:asyncio.Queue=None):
        # This coroutine generates 20 random input strings and populates the
        # output_q of whatever node it runs on.
        import uuid
        acc = [ str(uuid.uuid4()) for _ in range(20) ]
        for i in acc:
            await output_q.put(i)
            # unnecessary but async
            await asyncio.sleep(0)
	
    @classmethod
    async def output_coro(cls, self, q_elt):
        print('output~> ', q_elt)
		

async def main():
	input_d = {
	    'nodes': {
	        'inp': { 'coro': StringFuncs.input_coro },
	        'rev': { 'coro': StringFuncs.reverse },
	        'out': { 'coro': StringFuncs.output_coro },
	    },
	    'graph': {
	        'inp': ('rev', 'out'),  # output of node 'inp' ~> 'rev' and 'out'
	        'rev': ('out', ),       # and so on...
	        'out': None,
	    },
	}

	_t = Plumber(input_d, coro_map=lambda x: x)
	_t.create_pipeline()


if __name__ == '__main__':
	loop.create_task(main())
	loop.run_forever()
