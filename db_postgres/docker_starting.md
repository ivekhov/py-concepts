source 
https://scriptable.com/postgresql/how-to-install-postgresql-mac-docker/

1 Creating docker image:
`$ docker run --name postgres-container -e POSTGRES_PASSWORD={see in .env} -p 5432:5432 -v postgres-data:/var/lib/postgresql/data -d postgres`

2 List of dockers:
`$ docker ps`

Access: 
`$ docker exec -it postgres-container psql -U postgres`



