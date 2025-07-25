#!/bin/bash

LANG=$1
CODE_FILE=$2
INPUT_FILE=$3
OUTPUT_NAME=$4
TIME_LIMIT=$5    # seconds
MEMORY_LIMIT=$6  # MB

OUTPUT_FILE="/output/$OUTPUT_NAME"
echo "Writing to: $OUTPUT_FILE"
echo "Some output" > "$OUTPUT_FILE"


cd /runner || exit 1

# Reject unexpected file paths
[[ "$CODE_FILE" != /runner/* ]] && echo "Invalid code path" && exit 1
[[ "$INPUT_FILE" != /runner/* ]] && echo "Invalid input path" && exit 1
[[ "$OUTPUT_FILE" != /output/* ]] && echo "Invalid output path" && exit 1


# Don't run as root
if [ "$(id -u)" -eq 0 ]; then
  echo "Unsafe: Running as root. Aborting." > "$OUTPUT_FILE"
  exit 1
fi

# Validate code path
if [[ "$CODE_FILE" != /runner/* ]]; then
  echo "Invalid code path" > "$OUTPUT_FILE"
  exit 1
fi

# Set up executable output file path
EXEC_FILE="/runner/code_exec"

# Compile if needed
if [ "$LANG" == "c" ]; then
    gcc "$CODE_FILE" -o "$EXEC_FILE"
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1

elif [ "$LANG" == "cpp" ]; then
    g++ "$CODE_FILE" -o "$EXEC_FILE"
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1

elif [ "$LANG" == "java" ]; then
    javac "$CODE_FILE"
    [[ $? -ne 0 ]] && echo "Compilation Error" > "$OUTPUT_FILE" && exit 1
fi

# Apply memory limit
ulimit -v $((MEMORY_LIMIT * 1024))

# Safe execution wrapper
run_command() {
    if ! timeout --preserve-status "$TIME_LIMIT" bash -c "$1" < "$INPUT_FILE" > "$OUTPUT_FILE" 2>/runner/stderr.log; then
        status=$?
        if [ "$status" -eq 124 ] || [ "$status" -eq 137 ]; then
            echo "Time Limit Exceeded" > "$OUTPUT_FILE"
        else
            echo "Runtime Error" > "$OUTPUT_FILE"
        fi
    fi
}

# Run based on language
case "$LANG" in
  python)
    run_command "python3 $CODE_FILE"
    ;;
  c|cpp)
    run_command "$EXEC_FILE"
    ;;
  java)
    run_command "java -Xmx${MEMORY_LIMIT}m Main"
    ;;
  *)
    echo "Unsupported language" > "$OUTPUT_FILE"
    exit 1
    ;;
esac
