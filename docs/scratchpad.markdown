## Scratchpad

### class `Plumber`

```
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
```

