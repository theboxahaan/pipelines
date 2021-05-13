import asyncio
import logging
import traceback

from . import processor

class Plumber:
	"""
	Class that instruments Processor instances and creates data pipelines according
	to the provided graph.
	
	Input
	-----
	1. input_d:dict - This dictionary specifies the graph and node configurations
	   input_d = {
	       'nodes': {
		       'node_name'<str> : {'coro':<str>/<object>,
			                       'args':{<arguments to the specified coro>},
								  },
			   ...
		   },
		   'graph': {
		       'node_name'<str> : ('node_name_1', ...) <tuple of node names> or None,
			   ...
		   }
	   }
	2. coro_map: callable function - A function that maps the input_d['nodes'][<key>] object
	                                 to a callable function object with the following signature.
	   
	   def callable(coro_name:object) -> function(self:Processor, q_elt or q_out, **args)
	   
	   :. Here `self` refers to the Processor object on which the coro is running, `q_elt` is
	      an item from the input queue (or it is the output_queue in which data is to be pushed
		  for InputProcessor)
	"""


	def __init__(self, input_d:dict=None, coro_map=None):
		self.__liason_q_graph   = None 
		self.__node_list        = []
		self.__primary_input_q  = [asyncio.Queue()]
		self.__primary_output_q = [asyncio.Queue()]
		self.__coro_map         = coro_map

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
			for _i, (node_name,node_d) in enumerate(nodes_d.items()):
				c_input_srcs = [ liason_g[i][_i] for i in range(len(nodes_d)) if liason_g[i][_i] is not None]
				c_output_dests = [ i for i in liason_g[_i] if i is not None ]
				kwargs=dict(name=node_name, 
						coro=self.__coro_map(node_d['coro']), 
						input_srcs=c_input_srcs,
						output_dests=c_output_dests)
				f_kwargs=node_d.get('args', {})		
				logging.info('%s has f_kwargs %s', node_name, f_kwargs)
				if c_input_srcs == []:
					_n = processor.InputProcessor(**kwargs, **f_kwargs)
				else:
					_n = processor.Processor(**kwargs, **f_kwargs)
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
		try:
			ig = [[ None for i in range(len(input_d))] for j in range(len(input_d))]

			for input_node, output_node_list in input_d.items():
				if output_node_list is None:
					continue
				for node in output_node_list:
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
