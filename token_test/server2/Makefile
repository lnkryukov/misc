
.PHONY: run kill test

run: server.PID

server.PID:
	gunicorn main:app -b 0.0.0.0:4000 & echo $$! > $@
	sleep 1

kill: server.PID
	kill -9 `cat $<` && rm $<
	sleep 10

clean: 
	rm server.PID

test: run
	curl --header "Content-Type: application/json"   --request POST   --data '{"username":"first","password":"abcd"}'   http://127.0.0.1:4000/getToken