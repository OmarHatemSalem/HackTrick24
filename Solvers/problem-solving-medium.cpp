#include <iostream>
#include <stack>
#include <string>
#include <cctype>

using namespace std;

string decodeString(const string &s)
{
    stack<int> counts;
    stack<string> resultStack;
    string result = "";
    int index = 0;

    while (index < s.length())
    {
        if (isdigit(s[index]))
        {
            int count = 0;
            while (isdigit(s[index]))
            {
                count = 10 * count + (s[index] - '0');
                index++;
            }
            counts.push(count);
        }
        else if (s[index] == '[')
        {
            resultStack.push(result);
            result = "";
            index++;
        }
        else if (s[index] == ']')
        {
            string temp = resultStack.top();
            resultStack.pop();
            int count = counts.top();
            counts.pop();
            for (int i = 0; i < count; i++)
            {
                temp += result;
            }
            result = temp;
            index++;
        }
        else
        {
            result += s[index];
            index++;
        }
    }

    return result;
}

int main()
{
    string encodedString;
    cout << "Enter the encoded string: ";
    cin >> encodedString;
    cout << "Decoded string: " << decodeString(encodedString) << endl;
    return 0;
}