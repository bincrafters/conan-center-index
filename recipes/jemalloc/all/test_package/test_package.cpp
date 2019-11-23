#include <stdlib.h>
#include <jemalloc/jemalloc.h>

void do_something(size_t i) {
        malloc(i * 100);
}

int main() {
	for (size_t i = 0; i < 1000; i++) {
			do_something(i);
	}
	je_malloc_stats_print(NULL, NULL, NULL);
	return 0;
}