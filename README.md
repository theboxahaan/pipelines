## `pipelines` -- Create Async Processing Pipelines Quick


### class `Processor`
```
                           ┌-----------------------[Processor]---------------------------┐     
 ┌---------┐         ┌-----└---┐                                                    ┌----┘----┐
 | inputQ1 |  ---->  |         |      ┌-------------┐         ┌--------------┐      |         |
 └---------┘         |  input  | ---> | input_queue |         | output_queue | ---> | output  |
                     | handler |      └-------------┘         └--------------┘      | handler |
 ┌---------┐         |         |        |     ┌----------------┐    ^               |         |
 | inputQ2 |  ---->  |         |        └---> | processor_coro | ---┘               |         |
 └---------┘         └----┐----┘              └----------------┘    ┌-------------┐ └----┐----┘
                          |                                         | accumulator |      |     
                          └-----------------------------------------└-------------┘------┘     
```
### Demo
**Prerequisites** - `socketio`, `aiohttp` 

To run the demo navigate to `demos` directory and execute the followingi-

*To start the Server*
```python
$ python server.py
```
*To start the Client*
```python
$ python client.py
```

#### Points to Keep in Mind
1. `processor_coro` can be configured only once i.e. function factories are unsupported ??

### Test
```bash
# To test the Processor class 
$ python test_workflow.py

# To test the Plumber class
$ python test_plumber.py
```
The test does the following-
Set up a test rig for the `Processor` class. This is test rig plays the role of the `Plumber` *(hopefully)*
1. Create 2 `Processor` instances with the `reverse` and `append_reverse` coroutines resp.
2. The input to the `reverse` processor is a single queue, while the `append_reverse` processor takes input from 2 different queues.

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
