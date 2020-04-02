MAKEFLAGS := -j 2

run: run1 run2
kill: kill1 kill2
clean: clean1 clean2

kill1: 
	cd server1 && $(MAKE) kill
kill2:
	cd server2 && $(MAKE) kill

run1:
	cd server1 && $(MAKE) run
run2:
	cd server2 && $(MAKE) run

clean1:
	cd server1 && $(MAKE) clean
clean2:
	cd server2 && $(MAKE) clean