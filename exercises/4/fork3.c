/**
 * Explique el estado de los procesos hijos de este código.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *const argv[])
{
    if (fork() == 0) {
        return 0;
    }
    if (fork() == 0) {
        return 0;
    }

    printf("En otra pantalla ejecutar \"ps f\". Cualquier tecla para terminar \n");
    getchar();
    return 0;
}

