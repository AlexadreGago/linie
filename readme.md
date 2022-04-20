->docker build .

->docker run "docker image"

#Open another terminal
->docker exec -it "DOCKER CONTAINER ID" sh

->mongo
->show dbs

#Connect to mongo compass
mongodb://127.0.0.1:27017

#->docker network inspect bridge
#get the gateway ip
#go to /etc/mongod.conf
#on bindIp add the gateway ip example:     bindIp: 172.17.0.1