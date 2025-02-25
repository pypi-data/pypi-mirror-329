<!--- ==================================================================== --->

The context for
FIAT 
is somewhat standard for physical implementation, e.g.,
[side-channel](https://en.wikipedia.org/wiki/Side-channel_attack)
attacks.  At a (very) high level, it can be modelled as follows

```
+---------------------------+                 +--------------------------+
|          client           |                 |          target          |
+===========================+                 +==========================+
|                           | ----- req ----> | kernel layer             |
|                           | <---- ack ----- |~~~~~~~~~~~~~~~~~~~~~~~~~~|
|                           |                 | driver layer: SPRs, GPRs |
|                           |                 |~~~~~~~~~~~~~~~~~~~~~~~~~~|
|                           | <-- trigger --- |  board layer: UART, GPIO |
+---------------------------+                 +--------------------------+
```

in the sense that there are two parties,
a client (or user)
and
a target,
who interact synchronously:
the client transmits a  req(uest)         to the target,
the target performs some computation,
then
the target transmits an ack(nowledgement) to the client,
FIAT structures the target implementation into

1. a kernel layer, 
   i.e., the use-case specific functionality of interest,
2. a  board layer,
   i.e., infrastructure related to the hardware, or board said functionality is executed on,
3. a driver layer,
   which uses the board layer to provide an interface to the kernel,

noting the state is reflected by a set of special- and general-purpose 
registers.  The goal is to support both

- the target implementation, e.g., by providing 
  the board and driver layers, plus a build system, meaning the developer need only configure and implement the kernel layer,
  and
- the client implementation, e.g., by providing 
  a library that manages low-level interaction with a given target implementation,

while at least *attempting* to balance simplicity against flexibility.

<!--- ==================================================================== --->
