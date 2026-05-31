#include <iostream>
#include <string>
using namespace std;

int main() {
    string text;
    int count = 0;

    cout << "문자열 입력 >> ";
    
getline(cin, text);

for (int i = 0; i < text.length(); i++) {
        if (text[i] == 'a') {
            count++;
        }
    }

    cout << "문자 a는 " << count << "개 있습니다." << endl;

    return 0;
}
