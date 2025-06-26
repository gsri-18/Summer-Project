#include <iostream>
using namespace std;

int main() {
    const int N = 100000000;  // 100 million ints = ~400MB
    int* arr = new(nothrow) int[N];  // Use nothrow to avoid crash on allocation failure

    if (!arr) {
        cout << "Memory allocation failed" << endl;
        return 1;
    }

    for (int i = 0; i < N; ++i)
        arr[i] = i;

    cout << arr[0] << endl;
    delete[] arr;
    return 0;
}
