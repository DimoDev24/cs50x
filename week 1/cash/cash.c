#include <cs50.h>
#include <stdio.h>

int main(void)
{

    int cash = 0;
    int coin = 0;

    do
    {
        cash = get_int("Change owed: ");
    }
    while (cash <= 0);

    while (cash > 0)
    {
        if (cash >= 25)
        {
            cash -= 25;
            coin++;
        }
        else if (cash >= 10)
        {
            cash -= 10;
            coin++;
        }
        else if (cash >= 5)
        {
            cash -= 5;
            coin++;
        }
        else
        {
            cash--;
            coin++;
        }
    }

    printf("%i\n", coin);

    return 0;
}
