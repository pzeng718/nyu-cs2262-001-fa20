1. use "docker network create N_NAME" to create a network that three services that communicate through
2. when running docker images add "--netowrk N_NAME" 
3. when specifying corresponding IP use the name of the container, for example, if you run AS container through command "docker run --network N_NAME --name AS -p
53533:53533/udp -it bulutmf/as:latest", you should put as_ip as "AS"