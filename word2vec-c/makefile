SCRIPTS_DIR=../scripts
BIN_DIR=../bin

CC = gcc
#The -Ofast might not work with older versions of gcc; in that case, use -O2
CFLAGS = -lm -pthread -O2 -Wall -funroll-loops

all: word2vec word2phrase w2v-distance w2v-word-analogy w2v-compute-accuracy

word2vec : word2vec.c
	$(CC) word2vec.c -o ${BIN_DIR}/word2vec $(CFLAGS)
word2phrase : word2phrase.c
	$(CC) word2phrase.c -o ${BIN_DIR}/word2phrase $(CFLAGS)
w2v-distance : distance.c
	$(CC) distance.c -o ${BIN_DIR}/w2v-distance $(CFLAGS)
w2v-word-analogy : word-analogy.c
	$(CC) word-analogy.c -o ${BIN_DIR}/w2v-word-analogy $(CFLAGS)
w2v-compute-accuracy : compute-accuracy.c
	$(CC) compute-accuracy.c -o ${BIN_DIR}/w2v-compute-accuracy $(CFLAGS)

clean:
	pushd ${BIN_DIR} && rm -rf word2vec word2phrase distance word-analogy compute-accuracy; popd
