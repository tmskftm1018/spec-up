#include <iostream>
#include <string>

using namespace std;

class Person {
    int id;
    double weight;
    string name;
public:
    Person() {
        id = 1;
        weight = 20.5;
        name = "Grace";
    }

    Person(int i, string n) {
        id = i;
        name = n;
        weight = 20.5;
    }

    Person(int i, string n, double w) {
        id = i;
        name = n;
        weight = w;
    }

    void show() {
        cout << id << " " << weight << " " << name << endl;
    }
};

int main() {

    Person grace, ashley(2, "Ashley"), helen(3, "Helen", 32.5);

    grace.show();
    ashley.show();
    helen.show();
}
