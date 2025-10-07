#!/bin/bash

models=("llama3.2" "bge-m3")
n=${#models[@]}

result=0
while [ $result -lt $n ]; do
    result=0
    for model in "${models[@]}"; do
        ready=$(curl ollama:11434/api/show -d '{"name": "'"$model"'"}' | grep "not found" | wc -l)
        ready=$((1-ready))
        result=$((result + ready))
    done
    sleep 5
done

