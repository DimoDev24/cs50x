#import <cs50.h>
#import <stdio.h>

int main(void)
{
    string nombre = get_string("What's your name? ");

    printf("Hello, %s\n", nombre);
}
