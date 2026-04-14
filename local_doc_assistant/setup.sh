#!/bin/bash
python3 -m venv envi
source envi/bin/activate
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve &
    sleep 3
fi

MODELS=("qwen3:8b" "qwen3-embedding:4b")

for MODEL in "${MODELS[@]}"; do
    if ollama list | grep -q "$MODEL"; then
        echo "Модель $MODEL уже установлена."
    else
        echo "Скачиваю $MODEL..."
        ollama pull "$MODEL"
    fi
done

pip install -r requirements.txt
python3 local-doc-assistant.py
