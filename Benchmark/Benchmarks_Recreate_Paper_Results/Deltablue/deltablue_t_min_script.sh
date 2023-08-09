#!/bin/bash

# Loop 10 times
for ((i=1; i<=10; i++))
do
    echo "Iteration $i"
    echo "---------------------------------------"
    
    echo "T-Min-SP-JIT-SF"
    time ./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_deltablue_static_basic.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame -X install-strict-loader Tools/benchmarks/deltablue_static_basic.py 100
    
    echo "T-Min-SP-JIT"
    time ./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_deltablue_static_basic.txt -X jit-enable-jit-list-wildcards -X install-strict-loader Tools/benchmarks/deltablue_static_basic.py 100
    
    echo "T-Min-SP"
    time ./python.exe -X install-strict-loader Tools/benchmarks/deltablue_static_basic.py 100
    
    echo "T-Min-JIT-SF"
    time ./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_deltablue_static_basic.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame Tools/benchmarks/deltablue_static_basic.py 100
    
    echo "T-Min-JIT"
    time ./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_deltablue_static_basic.txt -X jit-enable-jit-list-wildcards Tools/benchmarks/deltablue_static_basic.py 100
    
    echo "T-Min"
    time ./python.exe Tools/benchmarks/deltablue_static_basic.py 100

    echo "---------------------------------------"

done

echo "All iterations completed"
