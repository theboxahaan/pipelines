from test_workflow import StringFunc 
import asyncio

def getcoro(name):
	d = {
		'StringFunc.reverse' : StringFunc.reverse,
		'StringFunc.toupper' : StringFunc.toupper,
		'StringFunc.tolower' : StringFunc.tolower,
		'StringFunc.input_str': StringFunc.input_str,
		'StringFunc.output_str': StringFunc.output_str,

	}

	if callable(name):
		return name
	else:
		return d[name]


if __name__ == '__main__':
	print(getcoro('StringFunc.reverse'))
