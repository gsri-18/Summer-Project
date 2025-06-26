#include <iostream>
using namespace std;

int main() {
    int* arr = new int[1e8]; // 100 million ints ~ 400MB
    for (int i = 0; i < 1e8; i++) arr[i] = i;
    cout << arr[0] << endl;
    delete[] arr;
    return 0;
}
