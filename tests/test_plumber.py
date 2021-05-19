import asyncio
from pipelines.plumber import Plumber
from test_workflow import StringFunc
from pipelines.utils import getcoro

async def main():
	input_d = {
		'nodes': {
			'inp': {'coro': StringFunc.input_str, 'args': { 'num': 20 }},
			'n1' : {'coro': StringFunc.reverse }, 
			'n2' : {'coro': 'StringFunc.toupper'},
			'n3' : {'coro': 'StringFunc.tolower'},
			'n4' : {'coro': 'StringFunc.output_str', 'properties': {'aggregate_inputs': False}},
		},
		'graph': {
			'inp': ('n1',),
			'n1' : ('n2', 'n3'),
			'n2' : ('n3', 'n4'),
			'n3' : ('n4',),
			'n4' : None,
		},
	}

	_t = Plumber(input_d, coro_map = getcoro )
	for _q in _t.nodes:
		print(f':. name ~> {_q.name}., input ~> {_q.liason_queues[0]}, output~> {_q.liason_queues[1]}')
	
	for _q in _t.nodes:
		print(f":. name ~> {_q.name}, coro ~> {_q.processor_coro}")


if __name__ == '__main__':
	asyncio.get_event_loop().create_task(main())
	asyncio.get_event_loop().run_forever()
