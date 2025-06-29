#!/bin/bash

LANG=$1
CODE_FILE=$2
INPUT_FILE=$3
OUTPUT_FILE=$4
TIME_LIMIT=$5
MEMORY_LIMIT=$6

cd /runner || exit 1

# ✅ 1. Compile WITHOUT any memory limits
if [ "$LANG" == "c" ]; then
    gcc "$CODE_FILE" -o code_exec
    if [ $? -ne 0 ]; then
        echo "Compilation Error" > "$OUTPUT_FILE"
        exit 1
    fi

elif [ "$LANG" == "cpp" ]; then
    g++ "$CODE_FILE" -o code_exec
    if [ $? -ne 0 ]; then
        echo "Compilation Error" > "$OUTPUT_FILE"
        exit 1
    fi

elif [ "$LANG" == "java" ]; then
    javac "$CODE_FILE"
    if [ $? -ne 0 ]; then
        echo "Compilation Error" > "$OUTPUT_FILE"
        exit 1
    fi
fi

# ✅ 2. Now apply memory limits ONLY for execution
ulimit -v $((MEMORY_LIMIT * 1024))

# ✅ 3. Execution phase
if [ "$LANG" == "python" ]; then
    timeout "$TIME_LIMIT" python3 "$CODE_FILE" < "$INPUT_FILE" > "$OUTPUT_FILE"

elif [ "$LANG" == "c" ] || [ "$LANG" == "cpp" ]; then
    timeout "$TIME_LIMIT" ./code_exec < "$INPUT_FILE" > "$OUTPUT_FILE"

elif [ "$LANG" == "java" ]; then
    timeout "$TIME_LIMIT" java -Xmx${MEMORY_LIMIT}m Main < "$INPUT_FILE" > "$OUTPUT_FILE"

else
    echo "Unsupported language" > "$OUTPUT_FILE"
    exit 1
fi
