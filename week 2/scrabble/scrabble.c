#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int sum_score(string word);

int main(void)
{
    // Ask 2 words and make an array
    string word1 = get_string("Player1: ");
    string word2 = get_string("Player2: ");

    // Dividir palabras en carácteres y ponerlos mayuscula
    int score1 = sum_score(word1);
    int score2 = sum_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 Wins!!\n\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 Wins!!\n\n");
    }
    else
    {
        printf("It's a Tie!!\n\n");
    }
}

int sum_score(string word)
{
    int score = 0;
    int len = strlen(word);

    for (int i = 0; i < len; i++)
    {
        if (isupper(word[i]))
        {
            score += points[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += points[word[i] - 'a'];
        }
    }
    return score;
}
