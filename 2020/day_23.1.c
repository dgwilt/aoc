#include <stdio.h>
#include <stdlib.h>

int ctoi(char c) {
    return c - '0';
}

int main( ) {
    const int NCUPS = 1000000;
    const int MOVES = 10000000;
    char data[9] = "219347865";
    int *cups = malloc((NCUPS+1) * sizeof(int));
    int start, end, pre, post, mid;
    int dst,fr,to;

    for (unsigned i=1;i<=NCUPS;i++) {
        fr = (i <= 9) ? ctoi(data[i-1]) : i;
        to = (i >= 9) ? i+1 : ctoi(data[i]);
        if (to >= 1 && to <= NCUPS && fr >= 1 && fr <= NCUPS) {
            cups[fr] = to;
        }
    }

    // Not using position 0!
    to = ctoi(data[0]);
    fr = (NCUPS <= 9) ? ctoi(data[NCUPS-1]) : NCUPS;
    cups[fr] = to;

    int label = ctoi(data[0]);
    for (int i=0;i<MOVES;i++) {

        pre = label;
        start = cups[pre];

        mid = cups[start];
        end = cups[mid];
        post = cups[end];

        cups[pre] = post;

        dst = label;
        while (1) {
            dst--;
            if (dst == 0) { dst = NCUPS; }
            if (dst != start && dst != mid && dst != end) { break; }
        }

        pre = dst;
        post = cups[pre];

        cups[pre] = start;
        cups[end] = post;

        label = cups[label];

    }
    unsigned long long v1 = cups[1];
    unsigned long long v2 = cups[v1];
    printf("%llu\n",v1*v2);
    free(cups);
    return 0;
}
