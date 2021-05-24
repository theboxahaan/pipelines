# `pipelines` -- Create Async Processing Pipelines Quick!
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

<img src="https://user-images.githubusercontent.com/32961084/119255818-539d9400-bbdb-11eb-9df1-26633a1021e7.png" width=46% align=right>

## What is it ?
`pipelines` is a library to help developers create async processing pipelines quickly and effortlessly. The motivation being - 
> The developer should only be worried about defining coroutines that do the actual processing.

## How does it work ?
A processing pipeline is represented as a directed graph of nodes where each node represents a *processor*. Think of it like a state machine. Each processor has associated with it a coroutine that performs some arbitrary operation on data. That operation could be anything from - reversing a string, querying a database to sending raw data to a cluster for processing.

The `Plumber` class object is responsible for building *processor-consumer* connections between different `Processor`'s. It creates the pipeline based on an input graph and instantiates the `Processor`s.

---------------

### Demo
**Prerequisites** - `socketio`, `aiohttp` 

To run the demo navigate to `demos` directory and execute the following-
> *The server is bound to port `8080`*

```bash
# To start the server
$ python server.py

# To start the client
$ python client.py
```
Most of the coroutines have an `asyncio.sleep()` call to simulate an IO bound wait...

### Test
```bash
# To test the Processor class 
$ python test_workflow.py

# To test the Plumber class
$ python test_plumber.py
```
The `test_workflow.py` does the following-
Set up a test rig for the `Processor` class. This is test rig plays the role of the `Plumber` *(hopefully)*
1. Create 2 `Processor` instances with the `reverse` and `append_reverse` coroutines resp.
2. The input to the `reverse` processor is a single queue, while the `append_reverse` processor takes input from 2 different queues.

The pipeline set up in `test_plumber.py` is -

<img src="https://user-images.githubusercontent.com/32961084/119289456-4084d580-bc68-11eb-90d6-47a76a1d9fa9.png" width=45%>


--------------------

## API Description

Refer to the wiki [https://github.com/theboxahaan/pipelines/wiki/Processor](https://github.com/theboxahaan/pipelines/wiki/Processor)

-----------------

### Todo's
- [ ]  Add `doomsdayQueues` for clean task cancellation
- [x]  Finalise `Plumber` design
- [x]  Think about input specifications. Graph representations look good RN
- [ ]  Write a pipelines viewer if I get time.
- [x]  Write Input Rigs i.e. class with no inputQs and only outputs 
- [ ]  Add signal handler to handle script exit
- [x]  Add tests for Processor and Plumber
- [x]  Pass args through input ?
- [x]  Write a proper mechanism for getting function object from string~~
- [x]  `Plumber` is the only class that interacts with the established context. Need to find a way to make context variables available to `Processor` instances.~~
- [ ]  Make a `TypeVar` for Queues
- [ ]  **Write cleanup coros** -- first introduce types of Queues
- [x]  Write a demo with `aiohttp` or something...
- [x]  Add option for **non-aggregated** input for multi-input `Processor`s -- is there a need for this ??
- [ ]  Add an `Event` lock on `Processor`s to control pipelines.
- [ ]  Backpressure testing ??? How do I do that ?
- [ ]  Write documentation 
