# PYTIBRV 
PYTIBRV is a Python wrapper for TIBRV/C API

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
* Python API (aka PYTIBRV/API)   
 Most of TIBRV/C API are ported to PYTIBRV/API.   
 Before that, you must be familer with TIBRV/C API.  
 Naming convention is `tibrv` (lowercase), such as `tibrv_status, tibrvMsg, tibrvMsg_Create`
 
* Python Object Model (aka PYTIBRV/Object) 
 PYTIBRV provide object model, like as TIBRV/Java, which package TIBRV/C API to components.  
 Naming convention is `Tibrv` (capital), such as `TibrvStatus, TibrvMsg, TibrvListener`
 
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
status = tibrv_Open()
```


## Usage

PYTIBRV also rewrite TIBRV/C Examples to Python. Please refer to [examples](examples) for detail.  

[**Examples:**](examples/)  
* [tibrvsend](examples/api/tibrvsend.py) [PYTIBRV/Object](examples/python/tibrvsend.py)       
  Send Out a reliable RV message 

* [tibrvlisten](examples/api/tibrvlisten.py) [PYTIBRV/Object](examples/python/tibrvlisten.py)     
  Listen and display content of RV message for specific subject 
  
* [timer](examples/api/timer.py) [PYTIBRV/Object](examples/python/timer.py)    
  Demostrate TIBRV Timer / Callback / Closure  

* [tibrvfttime](examples/api/tibrvfttime.py) [PYTIBRV/Object](examples/python/tibrvfttime.py)     
  RVFT API, program support active/standby **AUTO-FAILOVER**, to send out RV message within timestamp.    

* [tibrvftmon](examples/api/tibrvftmon.py) [PYTIBRV/Object](examples/python/tibrvftmon.py)   
  RVFT API, program to monitor RVFT Members activities
  
* [tibrvcmsend](examples/api/tibrvcmsend.py) [PYTIBRV/Object](examples/python/tibrvcmsend.py)     
  Send out a certified RV message

* [tibrvcmlisten](examples/api/tibrvcmlisten.py) [PYTIBRV/Object](examples/python/tibrvcmlisten.py)  
  Listen and display content of certified RV message for multiple subjects 
  
* [tibrvdqlisten](examples/api/tibrvdqlisten.py) [PYTIBRV/Object](examples/python/tibrvdqlisten.py)  
  RVDQ API, program support **LOAD-SHARING**, to listen and display RV message for specific subjects. 


### TIBRV/C API 
All TIBRV/C API return tibrv_status to indicate the calling status.  
It use C POINTER(Call By Reference) to return created object handle. 

```C
// C in tibrv/msg.h 
tibrv_status tibrvMsg_Create(tibrvMsg * msg)

// in your code 
tibrv_status    status;
tibrvMsg        msg;
tibrv_i32       amt = 12345;

status = tibrvMsg_Create(&msg) 
if (TIBRV_OK != status) {
    // error handling 
}

status = tibrvMsg_UpdateI32(msg, "AMOUNT", amt);
...
```


### Python 
Python are all objects, there is no 'native' data type, like as C int/double. 

```Python
>>> x = int(123)
>>> type(x)
<class 'int'>
>>> 
``` 

And, Python is all 'Call By Refence',
more precisely, Python is '**Call By Reference of Object**'  
Unfortunately, Python 'Call By Reference' is immutable for most case,  
you **CAN'T** return a new object like as C POINTER.  

``` python
# Python 
def change(x):
    x = 'ABC'

...
y = '123'
change(y)
print(y)         # y is still '123'
```

When Python runing `x = 'ABC'` in change()  

It assign local variable x to a new string object reference.  
**Actually, local variable _x_ would be GC when change() returned**

-------------------------------------------------
In other way, Python support return as tuple.  
Rewrite TIBRV/C tibrvMsg_Create() to PYTIBRV/API

``` python 
# PYTIBRV/API 
def tibrvMsg_Create() -> (tibrv_status, tibrvMsg):
    # calling C API by ctypes 
    msg = ctypes.c_void_p()
    status = _rvlib.tibrvMsg_Create(ctypes.byref(msg)) 
    
    return status, msg.value 

...

status, msg = tibrvMsg_Create()     # return as tuple []
if status != TIBRV_OK:
    # error handling
    
status = tibrvMsg_UpdateI32(msg, 'AMOUNT', amt)

```

### Callback
In TIBRV/C, callback is declared as 

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
# Python 
def my_callback(event: int, messgae: int, closure: object):
   # do what you need
   status, sz = tibrvMsg_GetString(message, 'DATA') 
   
...

status, listener = tibrvEvent_CreateListener(que, my_callback, tx, '_RV.>', None)

```
  
  
Python3.6 support NewType and Callable from typing  

```Python
# Python 
from typing import NewType, Callable 

tibrv_status            = NewType('tibrv_status', int)              # int
tibrvId                 = NewType('tibrvId', int)                   # int
tibrvMsg                = NewType('tibrvMsg', int)                  # c_void_p
tibrvEvent              = NewType('tibrvEvent', int)                # tibrvId
tibrvDispatchable       = NewType('tibrvDispatchable', int)         # tibrvId
tibrvQueue              = NewType('tibrvQueue', int)                # tibrvId
...

tibrvEventCallback      = Callable[[tibrvEvent, tibrvMsg, object], None]

def tibrvEvent_CreateListener(que: tibrvQueue, callback: tibrvEventCallback, tx: tibrvTransport, 
                              subj: str, closure: object) -> tibrv_status:
    ...                              


def my_callback(event: tibrvEvent, messgae: tibrvMsg, closure: object):
   # do what you need
   status, sz = tibrvMsg_GetString(message, 'DATA') 
   
...

status, listener = tibrvEvent_CreateListener(que, my_callback, tx, '_RV.>', None)

```
  
  
Callback must be declared in module level,  
You **CAN'T** assign a class function(method) for callback.  
All Python class functions are pre-defined 'self' as 1'st parameter. 

```Python 
# in Python 
class MyApp:
    def my_callback(self, event, message, closure):
        # THIS IS NOT WORK 
```
  
Suggest to code as   
```Python
# in Python, use closure for your own reference. 
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
  
----------

I rewrite callback as Python Class, it is more strait forward.  
Please refer [examples/python/timer.py](examples/python/timer.py) 
or [examples/python/tibrvlisten.py](examples/python/tibrvlisten.py) for more detail.

### Data Types 
1. Python only provide bool, int, gloat, str as native data types,  
  Not likely as C, TIBRV/C support for I8, U8, I16, ..., I64, U64, F32, F64   
  
  Python ctypes support for all C native data type: I8 ... F64   
  **BUT ctypes DOES NOT PERFORM OVERFLOW CHECKING**   
  
  for exexample:   
  ```python 
  # In Python 
  # 0xFFF = int(4095) 
  status = tibrvMsg_UpdateI8(msg, 'I8', 0xFFF)        # -> I8 = -1 
  status = tibrvMsg_UpdateU8(msg, 'U8', 0xFFF)        # -> U8 = 255 
  ```

2. TIBRV/C Object Handle  
  TIBRV/C declare `tibrvId` as `tibrv_u32(unsigned int)`   
  `tibrvEvent, tibrvTransport, tibrvQueue, tibrvDispatcher` are all derived from `tibrvId`   
  `tibrvMsg` is actually a pointer to struct   
  
  In PYTIBRV/API, they are all declared as 'int'    
  
### Exception  
TIBRV/C API is 'exceptionless', beecause there is no Exception in C.  
You only need to check the returned code after calling.  
PYTIBRV/API is the same as TIBRV/C. You only need to check the returned code. 

PYTIBRV/Object is like as PYTIBRV/API mostly.  
You could check tibrv_status if there is a returned code.  
Or, you could access obj.error() to get last TibrvError. (like as C errno)  

```Python
# PYTIBRV/Object 
tx = TibrvTx()
status = tx.create(None, None, None)

# check return code
if status != TIBRV_OK:
    # erro handling

# there is no return code for property 
tx.description = 'TEST'
if tx.error() is not None:
    # error handling 
    print('ERROR', tx.error().code(), tx.error().text()) 
    
```

If you prefer Exception(try/except) Handling, 
you could set `TibrvStatus.exception(True)`. 
This would trigger TibrvError when tibrv_status is not TIBRV_OK. 

```Python 
# PYTIBRV/Object 
# enable exception handling
TibrvStatus.exception(True)

try:
    tx = TibrvTx()
    tx.create(None, None, None) 
    tx.description = 'TEST'
    
except TibrvErrr as er:
    # error handling 
    print('ERROR', er.code(), er.text())
    
```
  
## API


### TIBRV 

TIBRV/C | PYTIBRV/API | PYTIBRV/Object
--- | --- | --- 
`tibrv_Open()` | `tibrv_Open()` | `Tibrv.open()`
`tibrv_Close()` | `tibrv_Close()` | `Tirv.close()`
`tibrv_Version()` | `tibrv_Version()` | `Tibrv.version()`
  
 
```Python
# PYTIBRV/API 
status = tibrv_Open()
if status != TIBRV_OK:
    print('ERROR', status, tibrvStatus_GetText(status))
    sys.exit(-1)
```
  

```Python
#PYTIBRV/Object
status = Tibrv.open()
if status != TIBRV_OK:
    print('ERROR', status, TibrvStatus.text(status))
    sys.exit(-1)
```


### Status 
TIBRV/C | PYTIBRV/API | PYTIBRV/Object
--- | --- | --- 
 | | `class TibrvError(Exception)`
`tibrvStatus_GetText()` | `tibrvStatus_GetText()` | `TibrvStatus.text()` 
 | | `TibrvStatus.error()`
 | | `TibrvStatus.exception()`
  


 
### Message 
TIBRV/C | PYTIBRV/API | PYTIBRV/Object
--- | --- | --- 
`tibrvMsg_Create()`|`tibrvMsg_Create()`|`TibrvMsg.create()`
`tibrvMsg_Destroy()`|`tibrvMsg_Destroy()`|`TibrvMsg.destroy()`
`tibrvMsg_CreateCopy()`|`tibrvMsg_CreateCopy()`|`TibrvMsg.copy()`
`tibrvMsg_Detach()`|`tibrvMsg_Detach()`|`TibrvMsg.detach()`
`tibrvMsg_GetCurrentTime()`|`tibrvMsg_GetCurrentTime()`|`TibrvMsg.now()`
`tibrvMsg_GetNumFields()`|`tibrvMsg_GetNumFields()`|`TibrvMsg.count()`
`tibrvMsg_GetSendSubject()`|`tibrvMsg_GetSendSubject()`|`TibrvMsg.sendSubject`
`tibrvMsg_SetSendSubject()`|`tibrvMsg_SetSendSubject()`|`TibrvMsg.sendSubject`
`tibrvMsg_GetReplySubject()`|`tibrvMsg_GetReplySubject()`|`TibrvMsg.replySubject`
`tibrvMsg_SetReplySubject()`|`tibrvMsg_SetReplySubject()`|`TibrvMsg.replySubject`
`tibrvMsg_Reset()`|`tibrvMsg_Reset()`|`TibrvMsg.reset()`
`tibrvMsg_AddI8()`|`tibrvMsg_AddI8()`|`TibrvMsg.addI8()`
`tibrvMsg_AddU8()`|`tibrvMsg_AddU8()`|`TibrvMsg.addU8()`
`tibrvMsg_AddI16()`|`tibrvMsg_AddI16()`|`TibrvMsg.addI16()`
`tibrvMsg_AddU16()`|`tibrvMsg_AddU16()`|`TibrvMsg.addU16()`
`tibrvMsg_AddI32()`|`tibrvMsg_AddI32()`|`TibrvMsg.addI32()`
`tibrvMsg_AddU32()`|`tibrvMsg_AddU32()`|`TibrvMsg.addU32()`
`tibrvMsg_AddI64()`|`tibrvMsg_AddI64()`|`TibrvMsg.addI64()`
`tibrvMsg_AddU64()`|`tibrvMsg_AddU64()`|`TibrvMsg.addU64()`
`tibrvMsg_AddF32()`|`tibrvMsg_AddF32()`|`TibrvMsg.addF32()`
`tibrvMsg_AddF64()`|`tibrvMsg_AddF64()`|`TibrvMsg.addF64()`
`tibrvMsg_AddString()`|`tibrvMsg_AddString()`|`TibrvMsg.addStr()`
`tibrvMsg_AddMsg()`|`tibrvMsg_AddMsg()`|`TibrvMsg.addMsg()`
`tibrvMsg_AddDateTime()`|`tibrvMsg_AddDateTime()`|`TibrvMsg.addDateTime()`
`tibrvMsg_AddField()`|`tibrvMsg_AddField()`|`TibrvMsg.addField()`
`tibrvMsg_UpdateI8()`|`tibrvMsg_UpdateI8()`|`TibrvMsg.setI8()`
`tibrvMsg_UpdateU8()`|`tibrvMsg_UpdateU8()`|`TibrvMsg.setU8()`
`tibrvMsg_UpdateI16()`|`tibrvMsg_UpdateI16()`|`TibrvMsg.setI16()`
`tibrvMsg_UpdateU16()`|`tibrvMsg_UpdateU16()`|`TibrvMsg.setU16()`
`tibrvMsg_UpdateI32()`|`tibrvMsg_UpdateI32()`|`TibrvMsg.setI32()`
`tibrvMsg_UpdateU32()`|`tibrvMsg_UpdateU32()`|`TibrvMsg.setU32()`
`tibrvMsg_UpdateI64()`|`tibrvMsg_UpdateI64()`|`TibrvMsg.setI64()`
`tibrvMsg_UpdateU64()`|`tibrvMsg_UpdateU64()`|`TibrvMsg.setU64()`
`tibrvMsg_UpdateF32()`|`tibrvMsg_UpdateF32()`|`TibrvMsg.setF32()`
`tibrvMsg_UpdateF64()`|`tibrvMsg_UpdateF64()`|`TibrvMsg.setF64()`
`tibrvMsg_UpdateString()`<br>`tibrvMsg_UpdateStringArray()`|`tibrvMsg_UpdateString()`<br>`tibrvMsg_UpdateStringArray()`|`TibrvMsg.setStr()`
`tibrvMsg_UpdateMsg()`|`tibrvMsg_UpdateMsg()`|`TibrvMsg.setMsg()`
`tibrvMsg_UpdateDateTime()`|`tibrvMsg_UpdateDateTime()`|`TibrvMsg.setDateTime()`
`tibrvMsg_UpdateField()`|`tibrvMsg_UpdateField()`|`TibrvMsg.setField()`

### Event 

### Transport 

### Dispatcher 


## Contribute


## License
[GPLV2](LICENSE.md) 
