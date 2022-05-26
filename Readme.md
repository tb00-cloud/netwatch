# NetWatch

A simple network utility to periodically TCP test and track a set of targets on a specific port.

#### Important

This is a personal project and should not be considered production-ready. The source is currently maintained infrequently. You're free to use it in it's current state but use at your own risk.

#### Usage

See DockerHub
https://hub.docker.com/r/tb00/netwatch

Currently the only tag published is beta, usage of this tag means changes can be made unexpectedly as no version tags are currently being pushed.

#### Development

Full disclosure, this repo is rough around the edges. There is make file to assist but the build process needs clearing up. There are also currently no unit tests.

**When developing and testing locally**
Run `make dev up`. This will start up a MySQL container and run the python backend.
CD into the client directory.
Make a temporary change to the axios service base url to not use "/api/" and instead use "http://localhost:5000/api/". When running in "production", both the distribution and API sit behind Nginx - /api requests are forwarded to the backend API.
Run `yarn run serve`.

If you need to make a change to the backend, you will need to exit the running python module and re-run it with `make local-backend-run`.

**To publish**
Run `make build` followed by `make publish`. Be sure to set the client axios service base url back to "/api/"
