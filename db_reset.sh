#!/bin/bash
docker-compose rm -fv
docker volume ls -qf dangling=true | xargs -r docker volume rm
