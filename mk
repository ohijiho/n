CXXFLAGS += -O2 -Wall -lm -std=gnu++17
all: $n

run: $n input.txt
	./$< < $(word 2, $^)

ans.txt: $n input.txt
	./$< < $(word 2, $^) > $@

test: ans.txt output.txt
	diff $^

clean:
	rm -f $n $n.o

.PHONY: all clean test

%.input.txt: %.py
	python3 $< > $@

%.output.txt: ref.py %.input.txt
	python3 $@ < $(word 2, $^) > $@

%.ans.txt: $n %.input.txt
	./$< < $(word 2, $^) > $@

run.%: $n %.input.txt
	./$< < $(word 2, $^)

test.%: %.ans.txt %.output.txt
	diff $^

# phony run.% and test.%
