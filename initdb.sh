#!/bin/bash

docker rm -f bd1-distribuida
docker rm -f bd2-distribuida

docker run --name bd1-distribuida -e POSTGRES_PASSWORD=bd1-distribuida -p 5433:5432 -d postgres:latest

docker run --name bd2-distribuida -e POSTGRES_PASSWORD=bd2-distribuida -p 5434:5432 -d postgres:latest

function waitContainer {
  printf "Waiting for postgresql server to be up"
  attempt=0
  while [ $attempt -le 59 ]; do
    attempt=$(( $attempt + 1 ))
    printf "."
    result=$(docker logs --tail 2  bd1-distribuida 2>&1 )
    result2=$(docker logs --tail 2 bd2-distribuida 2>&1 )
    if grep 'database system is ready' <<< $result &&  grep 'database system is ready' <<< $result2; then
      echo "PostgreSQL is up!"
      break
    fi
    sleep 0.5
  done
}
waitContainer;
docker exec -it bd1-distribuida bash -c "dropdb -U postgres bd1-distribuida"
docker exec -it bd2-distribuida bash -c "dropdb -U postgres bd2-distribuida"
docker exec -it bd1-distribuida bash -c "createdb -E UTF8 -T template0 -U postgres bd1-distribuida"
docker exec -it bd2-distribuida bash -c "createdb -E UTF8 -T template0 -U postgres bd2-distribuida"

