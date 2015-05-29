Data Size  : 48.6 MB.


Number Of Process | Process Time | Read Time |  Write Time | real | user | sys 
--- | --- | ---  | --- | --- | --- | ---
2 | 4.5s | 0.16s | 23.51s | 32.343s | 36.796s | 27.727s
4 | 2.51s | 0.14s | 22.5s | 29.833s | 1m7.684s | 51.371s
8 | 1.45s | 0.13s | 23.45s | 29.483s | 2m5.724s | 1m46.477s
16| 0.93s | 0.15s | 21.75s | 29.286s | 3m47.122s | 3m27.157s
32| 0.6s | 0.16s | 31.11s | 47.050s | 9m52.244s | 10m24.401s

As the number of process increase, overhead for creating processes gets larger and unnegligible. 

For a small data set, the overhead is enormous compares to computing time.

Also as the number of process increase, the fluctuation of running times also incease, running times become very unstable.
