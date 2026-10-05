#import <cs50.h>
#import <stdio.h>

int main(void)
{
    // Variables out of the loops
    int height;
    int brick = 1;

    // Question to the user
    do
    {
        height = get_int("How big do you want to be the pyramid? ");
    }
    while (height < 1 || height > 8);

    // Creation of the pyramid
    while (height > 0)
    {
        for (int space = 1; space < height; space++)
        {
            printf(" ");
        }

        for (int i = 0; i < brick; i++)
        {
            printf("#");
        }

        printf("  ");

        for (int i = 0; i < brick; i++)
        {
            printf("#");
        }

        printf("\n");

        height--;
        brick++;
    }
}
