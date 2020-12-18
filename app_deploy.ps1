docker build . -t kevinmcgrath/comcon-user-update:1.1

docker tag kevinmcgrath/comcon-user-update:1.1 kevinmcgrath/comcon-user-update:latest

docker push kevinmcgrath/comcon-user-update:1.1
docker push kevinmcgrath/comcon-user-update:latest