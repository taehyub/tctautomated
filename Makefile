tctautomated_efl_mono.dll: tests/*.cs
	mcs -t:library $(shell pkg-config --libs efl-mono mono-nunit) -o:$@ $^

tests/*.cs:
	./autogen.py

clean:
	rm -rf tests/*.cs
