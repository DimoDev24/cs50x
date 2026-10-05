#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{

    if (argc < 2) {
        printf("ERROR: You need to specify the forensic file.\n");
        return 1;
    }
    if (argc > 2) {
        printf("ERROR: You put too many arguments.\n");
        return 1;
    }

    FILE *rawFile = fopen(argv[1], "r");

    if (rawFile == NULL) {
        printf("ERROR: The file is empty.\n");
        return 1;
    }

    FILE *outptr = NULL;
    BYTE buffer[512];
    char filename[8]={0};
    int njpeg = 0;

    while (fread(buffer, sizeof(BYTE)*512 , 1, rawFile) == 1) {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) {
            if (outptr != NULL) {
                fclose(outptr);
            }

            sprintf(filename, "%03d.jpg", njpeg++);
            outptr = fopen(filename, "w");
        }
        if (outptr != NULL) {
                fwrite(buffer, sizeof(BYTE)*512, 1, outptr);
        }
    }

    if (outptr != NULL) {
        fclose(outptr);
    }

    fclose(rawFile);

    return 0;

}
