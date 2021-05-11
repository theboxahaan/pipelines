import asyncio
from plumber import Plumber



async def main():
	input_d = {
		'nodes': {
			'n1' : 'StringFunc.reverse' ,
			'n2' : 'StringFunc.toupper',
			'n3' : 'StringFunc.tolower',
			'n4' : 'StringFunc.reverse',
		},
		'graph': {
			'n1' : ('n2', 'n3'),
			'n2' : ('n3', 'n4'),
			'n3' : ('n4',),
			'n4' : None,
		},
	}

	_t = Plumber(input_d)
	for _q in _t.nodes:
		print(f':. name ~> {_q.name}., input ~> {_q.liason_queues[0]}, output~> {_q.liason_queues[1]}')



if __name__ == '__main__':
	asyncio.run(main())
