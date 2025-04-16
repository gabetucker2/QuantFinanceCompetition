<h1>WELCOME TO THE ALGEBROS PROJECT</h1>

SCHEMATIC: https://lucid.app/lucidchart/99ecfd6f-5dfe-4e79-a7a0-e12c4c0d66b9/edit?viewport_loc=-11%2C-11%2C1299%2C848%2C0_0&invitationId=inv_3c36b8f3-85a9-4b5e-9f6f-10da5a832ae1

Noting that t0 means t, t1 means t-1, t2 means t-2, etc...

```
outer chunk (dictionary): {
    "inputs" (list of lists of floats): [
        [daOpen_t, clOpen_t],
        [daTarget_t1, daOpen_t1, clOpen_t1, clHigh_t1, clLow_t1, clClose_t1, clAdjClose_t1, clVolume_t1], # inner chunk
        [daTarget_t2, daOpen_t2, clOpen_t2, clHigh_t2, clLow_t2, clClose_t2, clAdjClose_t2, clVolume_t2],
        ...,
        [daTarget_tN, daOpen_tN, clOpen_tN, clHigh_tN, clLow_tN, clClose_tN, clAdjClose_tN, clVolume_tN],
    ]
    "target" (float): daTarget_t
}
```
