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
 └---------┘         └----┐----┘              └----------------┘                    └----┐----┘
                          |                                           accumulator        |     
                          └--------------------------------------------------------------┘     

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
1. Add `doomsdayQueues` for clean task cancellation
2. Finalise `Plumber` design
3. Think about input specifications. Graph representations look good RN.
4. Write a pipelines viewer if I get time.
5. Write Input Rigs i.e. class with no inputQs and only outputs 
6. Add signal handler to handle script exit
7. ~~Add tests for Processor and Plumber~~
