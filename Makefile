.PHONY:
build:
	docker build -t quay.io/ulrichschreiner/avr .

.PHONY:
dev:
	docker run -it --rm -p 8080:8080 -e KEY=$(KEY) -v $(PWD):/app -w /app --entrypoint bash quay.io/ulrichschreiner/avr

.PHONY:
poweron:
	curl "http://localhost:8080/srv/-60/Fritz7590>Internetradio>Rock-Antenne>Rock-Antenne%20Stream?key=$(KEY)"

.PHONY:
poweroff:
	curl "http://localhost:8080/off?key=$(KEY)"