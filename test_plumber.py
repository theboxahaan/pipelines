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
	for _ in _t.dump_nodes():
		print(f':. name ~> {_.name}., input ~> {_.dump_qs()[0]}, output~> {_.dump_qs()[1]}')



if __name__ == '__main__':
	asyncio.run(main())
