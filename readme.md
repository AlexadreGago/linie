->docker build .

#if docker not crated:
->`sudo docker run --name mongodb -d -p 27017:27017 mongo`
#if docker created:
->docker start "DOCKER CONTAINER ID"
#Open another terminal
->docker exec -it "DOCKER CONTAINER ID" sh

->mongo
->show dbs

#Connect to mongo compass
mongodb://127.0.0.1:27017

#->docker network inspect bridge # if you want to change mongo cantainer ip
#get the gateway ip
#go to /etc/mongod.conf
#on bindIp add the gateway ip example:     bindIp: 172.17.0.1

#to remove docker containers:
#docker-compose down
#docker rm -f $(docker ps -a -q)
#docker volume rm $(docker volume ls -q)
#docker rmi $(docker images -q)           