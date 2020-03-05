
.PHONY: run kill test

run: server.PID

server.PID:
	gunicorn main:app -b 0.0.0.0:5000 & echo $$! > $@
	sleep 1

kill: server.PID
	kill -9 `cat $<` && rm $<
	sleep 10

clean: 
	rm server.PID