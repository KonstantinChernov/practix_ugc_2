docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongo'

docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongo'

docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo'

docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongo'

docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongo'

docker exec -it mongors1n1 bash -c 'echo "use ugc" | mongo'

docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugc\")" | mongo'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc.marks\")" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc.marks\", {\"mark\": \"hashed\"})" | mongo'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc.reviews\")" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc.reviews\", {\"film_id\": \"hashed\"})" | mongo'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc.favorites\")" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc.favorites\", {\"film_id\": \"hashed\"})" | mongo'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc.review_likes\")" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc.review_likes\", {\"review_id\": \"hashed\"})" | mongo'