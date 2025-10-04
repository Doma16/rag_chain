#!/bin/sh

ollama serve &

sleep 5

while [ $(ps aux | grep ollama | wc -l) -lt 2]; do
  sleep 2
done

ollama pull bge-m3
ollama pull llama3.2

wait

