from test_workflow import StringFunc 

def getcoro(name:str):
	d = {
		'StringFunc.reverse' : StringFunc.reverse,
		'StringFunc.toupper' : StringFunc.toupper,
		'StringFunc.tolower' : StringFunc.tolower,
	}

	return d[name]


if __name__ == '__main__':
	print(getcoro('StringFunc.reverse'))
