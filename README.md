## `pipelines` -- Create Async Processing Piplines Quick



### class `Processor`
```
                           ┌-----------------------[Processor]---------------------------┐     
 ┌---------┐         ┌-----└---┐                                                    ┌----┘----┐
 | inputQ1 |  ---->  |         |      ┌-------------┐         ┌--------------┐      |         |
 └---------┘         |         | ---> | input_queue |         | output_queue | ---> |         |
                     |  input  |      └-------------┘         └--------------┘      |  output |
 ┌---------┐         | handler |        |     ┌----------------┐   ^                | handler |
 | inputQ2 |  ---->  |         |        └---> | processor_coro | --┘                |         |
 └---------┘         └----┐----┘              └----------------┘                    └----┐----┘
                          |                                           accumulator        |     
                          └--------------------------------------------------------------┘     

```


### Test
```python
$ python processor.py
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
