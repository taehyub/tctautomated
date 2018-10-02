tctautomated_efl_mono.dll: tests/*.cs
	mcs -t:library $(shell pkg-config --libs efl-mono) -o:$@ $^

tests/*.cs:
	./autogen.py
