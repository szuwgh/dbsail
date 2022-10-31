
all:main

main :
	docker build -t whg/python-dbsail:3.9.2 .
	docker container create --name dbsail whg/python-dbsail:3.9.2 .
	docker container cp dbsail:/opt/dbdata/dist/dbsail .
	docker container rm -f dbsail

.PHONY : clean
clean :
	docker rmi -f whg/python-dbsail:3.9.2 .
	docker container rm -f dbsail
	rm -rf dbsail