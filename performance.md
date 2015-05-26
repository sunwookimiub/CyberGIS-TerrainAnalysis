Data Size  : 48.6 MB.

Read Time  : 0.10304 s.

Write Time : 0.090349 s.

Number Of Process | Process Time | I\O time | real | user | sys 
--- | --- | ---  | --- | --- | ---
2 | 28.231s | 0.18s | 28.231s | 54.646s | 1.785s
4 | 16.520s | 0.15s | 16.620s | 1m0.840s | 1.610s
8 | 9.55s | 0.31s | 10.872s | 1m14.210s | 7.263s
8 | 13.63s | 0.18s | 40.097s | 1m54.739s | 17.218s
16| 5.11s | 0.19s | 8.962s | 1m26.850s | 17.305s 
32| 4.12s | 0.15s | 19.494s | 2m37.931s | 1m43.250s
32| 4.9s | 0.22s | 1m15.412s | 2m48.011s | 5m29.441s
64 | 3.49s | 0.21s | 1m29.167s | 3m51.992s | 9m59.128s

As the number of process increase, overhead for creating processes gets larger and unnegligible. 

For a small data set, the overhead is enormous compares to computing time.

Also as the number of process increase, the fluctuation of running times also incease, running times become very unstable.