#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int verify_bugs(int argc, string key);

int main(int argc, string argv[])
{
    string key = argv[1];
    string abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    if (verify_bugs(argc, key) == 1)
    {
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    int textlenght = strlen(plaintext);

    char ciphertext[textlenght];
    printf("ciphertext: ");

    for (int i = 0; i < textlenght; i++)
    {
        if (plaintext[i] >= 65 && plaintext[i] <= 122)
        {
            if (islower(plaintext[i]))
            {
                for (int j = 0; j < strlen(abc); j++)
                {
                    if (tolower(abc[j]) == plaintext[i])
                    {
                        ciphertext[i] = key[j];
                        printf("%c", tolower(ciphertext[i]));
                        j = 100;
                    }
                }
            }
            else if (isupper(plaintext[i]))
            {
                for (int j = 0; j < strlen(abc); j++)
                {
                    if (toupper(abc[j]) == plaintext[i])
                    {
                        ciphertext[i] = key[j];
                        printf("%c", toupper(ciphertext[i]));
                        j = 100;
                    }
                }
            }
        }
        else
        {
            printf("%c",plaintext[i]);
        }
    }

    // HACER DEBUG!!!!!!!!!!!!!!!!!!!

    printf("\n");

    return 0;

}

int verify_bugs(int argc, string key)
{
    // ERRORS
    // Number of parameters isn't > 2
    if (argc > 2)
    {
        printf("Error: You put more than one command-line argument.\n");
        return 1;
    }
    else if (argc < 2)
    {
        printf("Error: You need to put the key in the command-line argument.\n");
        return 1;
    }

    // Key isn't 26 characters
    if (strlen(key) != 26)
    {
        printf("Error: Your key must be 26 alphabetic characters.\n");
        return 1;
    }
    for (int i = 0; i < 26; i++)
    {
        // Key contain character not alphabetic
        if (key[i] < 65 || (key[i] > 90 && key[i] < 97) || key[i] > 122)
        {
            printf("Error: Your key must contain ONLY alphabetic characters.\n");
            return 1;
        }
        // for-loop to verify all keys
        for (int j = 0; j < i; j++)
        {
            // Key repeats characters
            if (key[i] == key[j] || tolower(key[i]) == tolower(key[j]))
            {
                printf("Error: Your key repeats an alphabetic character, it must contain all only once.\n");
                return 1;
            }
        }
    }

    return 0;
}
