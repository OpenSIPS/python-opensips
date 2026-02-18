# OpenSIPS Python Docker Image

Docker recipe for running a container with pre-installed OpenSIPS Python packages.

## Building the image
You can build the docker image by running:
```
make build
```

This command will build a docker image with OpenSIPS Python packages installed, along with 
`opensips-mi` and `opensips-event` command line tools.

## Parameters

The container receives parameters in the following format:
```
CMD [PARAMS]*
```

The meaning of the parameters is as follows:
* `CMD` - the command used to run; if the `CMD` ends with `.sh` extension, it
will be run as a bash script, if the `CMD` ends with `.py` extension, it is
run as a python script, otherwise it is run as a `opensips-mi` command
* `PARAMS` - optional additional parameters passed to `CMD`

## Run

To run a bash script, simply pass the connector followed by the bash script:
```
docker run --rm opensips/python-opensips:latest script.sh
```

Similarly, run a python script:
```
docker run --rm opensips/python-opensips:latest script.py
```

To run a single MI command, use:
```
docker run --rm opensips/python-opensips:latest -t datagram uptime
```

## DockerHub

Docker images are available on
[DockerHub](https://hub.docker.com/r/opensips/python-opensips).
