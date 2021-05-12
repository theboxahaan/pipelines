import asyncio
import logging
import traceback

from . import utils
from . import processor

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
	
	| input | --> | n1 | --> | n2 | --> | n3 | --> | n4 | --> | output |
	                |__________|__________^          ^
	                           |_____________________|
	"""
	def __init__(self, input_d:dict = None):
		self.__liason_q_graph = None 
		self.__node_list = []
		self.__primary_input_q = [asyncio.Queue()]
		self.__primary_output_q = [asyncio.Queue()]

		self._parse_input_graph(input_d['graph'])
		self._create_pipeline(input_d['nodes'], self.__liason_q_graph)

	@property
	def nodes(self) -> list:
		return self.__node_list
	
	@property
	def liason_graph(self):
		return self.__liason_q_graph

	def _create_pipeline(self, nodes_d:dict=None, liason_g:list=None):
	# caveat - the order of nodes in 'graph' and 'nodes' should be the same
		try:
			for _i, (node_name,node_coro) in enumerate(nodes_d.items()):
				c_input_srcs = [ liason_g[i][_i] for i in range(len(nodes_d)) if liason_g[i][_i] is not None]
				c_output_dests = [ i for i in liason_g[_i] if i is not None ]
				kwargs=dict(name=node_name, 
						coro=utils.getcoro(node_coro), 
						input_srcs=c_input_srcs,
						output_dests=c_output_dests)
				if c_input_srcs == []:
					_n = processor.InputProcessor(**kwargs)
				elif c_output_dests == []:
					_n = processor.Processor(**kwargs)
				else:
					_n = processor.Processor(**kwargs) 
				self.__node_list.append(_n) 
		
		except Exception as e:
			logging.error('[_create_pipeline]\n%s', traceback.format_exc())
			raise
	
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

			for input_node, output_node_list in input_d.items():
				if output_node_list is None:
					continue
				for node in output_node_list :
					index_k, index_i = list(input_d).index(input_node), list(input_d).index(node)
					ig[index_k][index_i] = asyncio.Queue()

			# now we have a 2D representation of the graph storing the liason Qs used
			# to hold intermediate messages btw nodes
			self.__liason_q_graph = ig
			logging.info('%s liason_q_graph\n%s', str(self), ig)
			#TODO add the graph diagram 
			
		except Exception as e:
			logging.error('%s', traceback.format_exc())
			raise
