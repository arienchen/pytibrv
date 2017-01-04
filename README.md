# PYTIBRV 
PYTIBRV is a Python wrapper for TIBRV C API

TIBCO Rendezvous® (aka TIBRV) is copyright of [TIBCO](www.tibco.com) 

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contribute](#contribute)
- [License](#license)

## Background
PYTIBRV use ctypes to call TIBRV/C API, It is not a Pyhton Extension.  
So, it is unnecessary to build/compile any C source for deployment.  

PYTIBRV contains 
* Python API  
 Most of TIBRV/C API are ported to PYTIBRV. You must be familer with TIBRV/C API.  
 Naming convention is ```tibrv``` (lowercase), such as ```tibrv_status, tibrvMsg, tibrvMsg_Create```
 
* Python Object Model  
 PYTIBRV provide object model, like as TIBRV/Java, which package TIBRV/C API to component.  
 Naming convention is ```Tibrv``` (capital), such as ```TibrvStatus, TibrvMsg, TibrvListener```
 
## Install
Copy pytibr/pytibrv into your Python packages directory,  
for example: $HOME/my_lib/
```
$HOME/my_lib/pytibrv/
                     __init__,py
                     api.py 
                     ...
```
> I am still working on setup.py 


Then, add $HOME/my_lib to PYTHONPATH

```shell
export PYTHONPATH=$HOME/my_lib
```

run python console to test

```python
from pytibrv.api import *
```


## Usage

PYTIBRV also rewrite TIBRV/C Examples to Python.
* tibrvsend
* tibrvlisten 
* tibrvcmsend 
* tibrvcmlisten 
* tibrvfttime 
* tibrvftmon 
* tibrvdqlisten 

Please refer to [examples](examples) for detail. 

### TIBRV/C API 
All TIBRV/C API return tibrv_status to indicate the calling status.  
It use C POINTER(Call By Reference) to return created object. 

```C
# in tibrv/msg.h 
tibrv_status tibrvMsg_Create(tibrvMsg * msg)


# in your code 
tibrv_status    status;
tibrvMsg        msg;
tibrv_i32       amt = 12345;

status = tibrvMsg_Create(&msg) 
if (TIBRV_OK != status) {
    # error handling 
}

status = tibrvMsg_UpdateI32(msg, "AMOUNT", amt);
...
```


### Python 
Python are all objects, there is no 'native' data type, like as C int/double. 

``` python
>>> x = int(123)
>>> type(x)
<class 'int'>
>>> 
``` 

And, Python is all 'Call By Refence',  
more precisely, Python is 'Call By Reference of Object'  
Unfortunately, Python 'Call By Reference' is immutable,  
you **CAN'T** return a new object like as C POINTER.  

``` python
def change(x):
    x = "ABC"

...
y = "123"
change(y)
print(y)         # y is still "123"
```

When Python runing ```x = "ABC"``` in change()  

It assign local variable x to a new string reference.  
Actually, x would be GC when change() returned

-------------------------------------------------

Python support return as tuple.  
Rewrite TIBRV/C tibrvMsg_Create() to Python

``` python 
def tibrvMsg_Create() -> (tibrv_status, tibrvMsg):
    # calling C API by ctypes 
    msg = ctypes.c_void_p()
    status = _rvlib.tibrvMsg_Create(ctypes.byref(msg)) 
    
    return status, msg.value 

...

status, msg = tibrvMsg_Create()     # return as tuple 
if status != TIBRV_OK:
    # error handling
    
status = tibrvMsg_UpdateI32(msg, 'AMOUNT', amt)

```

### Callback
In C, callback is declared as 
```C
typedef void (*tibrvEventCallback) (
                  tibrvEvent          event,
                  tibrvMsg            message,
                  void*               closure
                );
...

void my_callback(tibrvEvent event, tibrvMsg message, void * closure) {
    // do what you need 
    ...
}

...

status = tibrvEvent_CreateListener(&event, que, my_callback, tx, "_RV.>", NULL);

```

In Python, ALL is dynamic binding and no function typedef. 

```Python
def my_callback(event: int, messgae: int, closure: object):
   # do what you need
   status,sz = tibrvMsg_GetString(message, 'DATA') 
   
...

status, listener = tibrvEvent_CreateListener(que, my_callback, tx, '_RV.>', None)

```


Python3.6 support NewType and Callable from typing  
```Python
tibrv_status            = NewType('tibrv_status', int)              # int
tibrvId                 = NewType('tibrvId', int)                   # int
tibrvMsg                = NewType('tibrvMsg', int)                  # c_void_p
tibrvEvent              = NewType('tibrvEvent', int)                # tibrvId
tibrvDispatchable       = NewType('tibrvDispatchable', int)         # tibrvId
tibrvQueue              = NewType('tibrvQueue', int)                # tibrvId
...

tibrvEventCallback          = Callable[[tibrvEvent, tibrvMsg, object], None]
...

def my_callback(event: tibrvEvent, messgae: tibrvMsg, closure: object):
   # do what you need
   status,sz = tibrvMsg_GetString(message, 'DATA') 
   
...

status, listener = tibrvEvent_CreateListener(que, my_callback, tx, '_RV.>', None)

```

Callback must be declared in module level,  
You **CAN'T** assign a class function(method) as Callback.  
All class function are pre-defined 'self' as 1'st parameter. 

```Python 
class MyApp:
    def my_callback(self, event, message, closure):
        # THIS IS NOT WORK 
```

Suggest to code as   
```Python
def my_callback(event, message, closure):
    my_app = closure
    if my_app.flags == 0:
        ...
        
        
class MyApp:
    def __init__(self):
        self.flags = 0
        ...
        
    def init_rv(slef):
        # pass self as closure, to be accessed in callback 
        status, listener = tibrvEvent_CreateListener(que, my_callback, tx, '_RV.>', self) 
        
```
Please refer [examples/api/timer.py](examples/api/timer.py) 
or [examples/api/tibrvlisten.py](examples/api/tibrvlisten.py) for more detail.


I rewrite callback as Python Class, it is more strait forward.  
For PYTIBRV Object Model, Please refer [examples/python/timer.py](examples/python/timer.py) 
or [examples/python/tibrvlisten.py](examples/python/tibrvlisten.py) for more detail.

## API
### Data Types 

### TIBRV 

### Message 

### Event 

### Transport 

### Dispatcher 


## Contribute


## License
[GPLV2](LICENSE.md) 
