#!/bin/bash

LANG=$1
CODE_FILE=$2
INPUT_FILE=$3
OUTPUT_FILE=$4
TIME_LIMIT=$5    # in seconds
MEMORY_LIMIT=$6  # in MB

cd /runner || exit 1

# 🛠 1. Compile without memory/time limits
if [ "$LANG" == "c" ]; then
    gcc "$CODE_FILE" -o code_exec
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1

elif [ "$LANG" == "cpp" ]; then
    g++ "$CODE_FILE" -o code_exec
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1

elif [ "$LANG" == "java" ]; then
    javac "$CODE_FILE"
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1
fi

# 🧠 2. Setup memory and time limits
ulimit -v $((MEMORY_LIMIT * 1024))  # Set max virtual memory

# 🏃 3. Run the code with timeout and memory restrictions
run_command() {
    # Wrapper to handle timeout exit codes (124 = timeout, 137 = SIGKILL)
    if ! timeout --preserve-status "$TIME_LIMIT" bash -c "$1" < "$INPUT_FILE" > "$OUTPUT_FILE" 2>/runner/stderr.log; then
        status=$?
        if [ "$status" -eq 124 ] || [ "$status" -eq 137 ]; then
            echo "Time Limit Exceeded" > "$OUTPUT_FILE"
        else
            echo "Runtime Error" > "$OUTPUT_FILE"
        fi
    fi
}

if [ "$LANG" == "python" ]; then
    run_command "python3 $CODE_FILE"

elif [ "$LANG" == "c" ] || [ "$LANG" == "cpp" ]; then
    run_command "./code_exec"

elif [ "$LANG" == "java" ]; then
    run_command "java -Xmx${MEMORY_LIMIT}m Main"

else
    echo "Unsupported language" > "$OUTPUT_FILE"
    exit 1
fi
