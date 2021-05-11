import asyncio
import logging
import traceback

import utils
import processor

class Plumber:
	"""
	class Plumber - Helper class to contruct pipelines of Processors according
	to the specified input
	
	Input
	-----
	| input/output |    1    |    2    |    3    |    4    |
	--------------------------------------------------------
	|      1       |    x    |    v    |    v    |    x    |
	|      2       |    x    |    x    |    v    |    v    |
	|      3       |    x    |    x    |    x    |    v    |
	|      4       |    x    |    x    |    x    |    x    |
	
	or equivalently,

	|  input  |   outputs   |
	-------------------------
	|    1    |    2 , 3    |
	|    2    |    3 , 4    |
	|    3    |    4,       |
	|    4    |    None     |

	Above graph represents a pipeline where -
	
	|input| --> | n1 | --> | n2 | --> | n3 | --> | n4 | --> | output |
	              |__________|__________^          ^
	                         |_____________________|
	"""
	def __init__(self, input_d:dict):
		self.__liason_q_graph = None 
		self.__node_list = []
		self.__primary_input_q = [asyncio.Queue()]

		self._parse_input_graph(input_d['graph'])
		self._create_pipeline(input_d['nodes'], self.__liason_q_graph)

	def _create_pipeline(self, nodes_d:dict, liason_g:list):
	# caveat - the order of nodes in 'graph' and 'nodes' should be the same
		for _i, (k,v) in enumerate(nodes_d.items()):
			_n = processor.Processor(name=k, 
									 coro=utils.getcoro(v), 
									 input_srcs=self.__primary_input_q if _i==0 else [ liason_g[i][_i] for i in range(len(nodes_d)) if liason_g[i][_i] is not None],
									 output_dests=[ i for i in liason_g[_i] if i is not None ])
			self.__node_list.append(_n) 
			
	
	def _check_nodes(self, input_d:dict):
		try:
			pass
			# do the coro validation here
		except Exception as e:
			logging.error('%s', traceback.format_exc() )
			raise

	def _parse_input_graph(self, input_d:dict):
		# input_d := input_d[''graph]	
		# check for cycles skipped; will need to add later
		# check for bad nodes here i.e no inputs but outputs
		try:
			ig = [[ None for i in range(len(input_d))] for j in range(len(input_d))]

			for k,v in input_d.items():
				if v is None:
					continue
				for i in v :
					index_k, index_i = list(input_d).index(k), list(input_d).index(i)
					ig[index_k][index_i] = asyncio.Queue()

			# now we have a 2D representation of the graph storing the liason Qs used
			# to hold intermediate messages btw nodes
			self.__liason_q_graph = ig
			logging.info('%s liason_q_graph\n%s', str(self), ig)
			#TODO add the graph rendering
			
		except Exception as e:
			logging.error('%s', traceback.format_exc())
			raise

	def dump_nodes(self):
		return self.__node_list
