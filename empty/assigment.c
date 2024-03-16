#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#define n 3
void q5();
/*void q3();
void q2();
void q1(char str[]);
*/
int main()
{
    q5();
    return 0;

}
/*
void q1(char str[]) {

    for(int j=0;j<strlen(str)+1;j++){ if (isalpha(str[j]) != 0) printf("%c", (char)str[j]); }
}
void q2(){
    char input_str[500];
    fgets(input_str, sizeof(input_str), stdin);
    char newstr[26];
    memset(newstr, 0, sizeof(newstr));
    for (int i = 0; i < strlen(input_str); i++)
    {
        if(strchr(newstr,input_str[i])==NULL)
        newstr[strlen(newstr)] = input_str[i];
    }
    printf("%s\n", newstr);
}
void q3() {
    char input_str[500];
    fgets(input_str, sizeof(input_str), stdin);

    for (int i = 0; input_str[i] != '\0'; i++) {
        if (input_str[i] != '\0') {
            // Print the first occurrence
            printf("%c", input_str[i]);

            // Mark non-first occurrences
            for (int j = i + 1; input_str[j] != '\0'; j++) {
                if (input_str[j] == input_str[i]) {
                    input_str[j] = '\0';
                }
            }
        }
    }
}
*/
void q5() {
    char s[4] = { 'a','a','a',0 };
    int i, j, t;
    t = n * n * n;
    while (t--)
    {
        printf("%i\n", t);
        for (i = 0; i < n - 1; i++)
            printf("%1c", s[i]);
        printf("%1c\n", s[i]);
        if (++s[n - 1] > 'c')
        {
            s[t/n/4]++;
            for (j = n; j > 0; j--)
            {
                if (s[j-1]>'c')
                    s[j - 1] = 'a';
                else
                    break;

            }
        }
    }
}

