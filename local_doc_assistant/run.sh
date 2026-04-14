#!/bin/bash
if [ -z "$VIRTUAL_ENV" ]; then
    source envi/bin/activate
    if [ $? -ne 0 ]; then
        echo "Ошибка: убедитесь, что нужное окружение существует."
        exit 1
    fi
fi

if ! pgrep -x "ollama" > /dev/null; then
    ollama serve &
    sleep 3
fi

python3 local-doc-assistant.py 
