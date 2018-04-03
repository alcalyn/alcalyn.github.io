all: run logs

run:
	docker-compose up -d

logs:
	docker-compose logs -ft

stop:
	docker-compose stop

down:
	docker-compose down

restart: stop run logs

update: down run logs

bash:
	docker-compose up -d
	docker exec -ti alcalyn_jekyll bash
