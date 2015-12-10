BIN_DIR=../bin

CC=gcc
#Using -Ofast instead of -O3 might result in faster code, but is supported only by newer GCC versions
# CFLAGS=-lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result
CFLAGS=-lm -pthread -O3 -Wall -march=native -funroll-loops  -Wno-unused-result -I/usr/include/malloc # OS X

all: word2vec word2phrase distance word-analogy compute-accuracy

word2vec : word2vec.c
	$(CC) word2vec.c -o ${BIN_DIR}/word2vec $(CFLAGS)
word2phrase : word2phrase.c
	$(CC) word2phrase.c -o ${BIN_DIR}/word2phrase $(CFLAGS)
distance : distance.c
	$(CC) distance.c -o ${BIN_DIR}/w2v-distance $(CFLAGS)
word-analogy : word-analogy.c
	$(CC) word-analogy.c -o ${BIN_DIR}/w2v-word-analogy $(CFLAGS)
compute-accuracy : compute-accuracy.c
	$(CC) compute-accuracy.c -o ${BIN_DIR}/w2v-compute-accuracy $(CFLAGS)

clean:
	pushd ${BIN_DIR} && rm -rf word2vec word2phrase distance word-analogy compute-accuracy; popd
