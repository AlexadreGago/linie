->docker build .

->`sudo docker run --name mongodb -d -p 27017:27017 mongo`

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