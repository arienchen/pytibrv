# pytibrv
TIBCO Rendezvous® API for Python

TIBCO Rendezvous® is copyright of TIBCO www.tibco.com 

----------------------------------------------------------------------
<ol>
<li> 
pytibrv is a Python wraper to TIBRV/C API. 
it use ctypes rather than Python Extension.<br>
If low-latency is the main issue, please use C API, not in Python.
<br>
<li>
Develop and test for Python3.5+, not support for Python2
<br>
<li>
pytibrv follow the naming convension of TIBRV/C<br>
ex:<br>
<table>
<tr><td>C</td><td>Python</td></tr>
<tr><td>typedef int tibrv_status</td><td>tibrv_status = int</td></tr>
<tr><td>tibrv_status tibrv_Open()</td><td>def tibrv_Open() -> tibrv_status:</td></tr>
<tr><td>tibrv_status tibrv_Close()</td><td>def tibrv_Close() -> tibrv_status:</td></tr>
<tr><td>const cahr * tibrv_Version()</td><td>def tibrv_Version() -> str:</td></tr>
</table>
<br>
<li>
TIBRV/C use POINTER to return object<br>
ex:<br>
TIBRV/C 
<pre>
tibrv_statue tibrvMsg_Create(tibrvMsg * msg)<br>
...
tibrv_status    status;
tibrvMsg        msg;

status = tibrvMsg_Create(&msg) 
if (TIBRV_OK != status) {
  # error handling 
}
</pre>
Python support multiple return
<pre>
def tibrvMsg_Create() -> (tibrv_status, tibrvMsg):
  ...

# create msg
# you could check status == TIBRV_OK or msg == None 
status, msg = tibrvMsg_Create()
if status != TIBRV_OK:
  # error handling

if msg is None:
  # error handling
  
</pre>  

</ol> 

TO BE CONTINUE 
