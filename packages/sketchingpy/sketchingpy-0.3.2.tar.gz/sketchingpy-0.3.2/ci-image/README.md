# CI Image
Docker image for CI / CD as published at [sampottingersketching/sketchingci](https://hub.docker.com/repository/docker/sampottingersketching/sketchingci/general). To release:

 - Build: `docker build -t cicd .`
 - Tag: `docker image tag cicd sampottingersketching/sketchingci:v1.2`
 - Release: `docker image push sampottingersketching/sketchingci:v1.2`

This is used in CI / CD pipeline automatically.
