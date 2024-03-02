# Memory Tracker

To run this project in a `production`, it is necessary to install and configure `DockerSwarm`, as well as to create a `Node`.
### Create Network
Create a network with the driver `overlay`: <br/>
`docker network create --driver overlay mt-local` <br/>
`docker network create --driver overlay mt-public`
### Build the images
CD to the path `docker/Dockerfile` and run the following commands to create images:<br/>
`docker-compose build memory_tracker-fastapi` <br/>
`docker-compose build memory_tracker-nginx`

To run in the development mode, please run the following command, otherwise, continue the steps to the `Run` section.<br/>
`docker compose -f docker/docker-compose-dev.yml up` <br />
`curl -X GET http://localhost:8000/memory-logs/` <br />

For more information about the api, see 'endpoints' section.

### Environment Variables (production)
Create an environment variable with a username (you will use it for the HTTP Basic Auth for Traefik), for example:<br/>
``export USERNAME=hadi``<br/>
``export PASSWORD=do``<br/>

Use openssl to generate the "hashed" version of the password and store it in an environment variable:<br/>
``export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)``

### Run
CD to the path `memory_tracker/docker` and run the following commands to create and run stack: <br />
`docker stack deploy -c docker-compose-[deploy|dev].yml memory-tracker`

-----

### Docker Traefik Labels
docker-compose-deploy.yml
#### This section provides the Traefik labels configuration used for various purposes such as basic authentication, rate limiting, routing, and load balancing.
- `traefik.http.middlewares.api-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}`
  - Specifies basic authentication middleware for API access. Requires username and hashed password.
  
- `traefik.http.middlewares.api-ratelimit.ratelimit.burst=5`
  - Sets the burst rate for rate limiting to 5 requests.
  
- `traefik.http.middlewares.api-ratelimit.ratelimit.period=1m`
  - Sets the period for rate limiting to 1 minute.

- `traefik.http.routers.memory_tracker-http.rule=Host('logger.hadido.ir')`
  - Sets the rule for the HTTP router to route requests with the host 'logger.hadido.ir'.

- `traefik.http.routers.memory_tracker-http.middlewares=api-auth,api-ratelimit`
  - Specifies the middlewares to be applied to the HTTP router, including basic authentication and rate limiting.

- `traefik.http.services.memory_tracker.loadbalancer.server.port=80`
  - Sets the port for the load balancer server to 80 for the memory tracker service.
-----
### Memory Logger API Documentation
#### This API provides endpoints to retrieve memory usage logs.

### Endpoints
#### Retrieve Memory Logs [GET] <br/> 
``http://logger.hadido.ir/memory-logs/?limit=10&skip=3``

+ Headers (production)
  + `Authorization`: `Basic aGFkaTpkbw==`
  + {username: hadi, password: do}
+ Parameters
    + `limit` (optional, integer, `10`) ... Number of records to return from the end. Must be greater than 0 and less than 100,000.
    + `skip` (optional, integer) ... Number of records to skip. Must be greater than 0.


+ Response 200 (application/json)
    + Body
        ```
        [
          {
            "timestamp": 1647033600,
            "total": 8192,
            "free": 2048,
            "used": 6144
          },
          {
            "timestamp": 1647033700,
            "total": 8192,
            "free": 1024,
            "used": 7168
          }
        ]
        ```
+ Response 422 (application/json)
    + Body
        ```
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": [
                        "query",
                        "limit"
                    ],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "ten",
                    "url": "https://errors.pydantic.dev/2.6/v/int_parsing"
                }
            ]
        }
        ```
+ Response 404 (application/json)
    + Body
        ```
        {
          "detail": "Not Found."
        }
        ```
+ Response 405 (application/json)
    + Body
        ```
        {
          "detail": "Method Not Allowed."
        }
        ```
+ Response 500 (application/json)
    + Body
        ```
        {
          "detail": "Internal server error."
        }
        ```
----
### Configuration cronjob to run tasks.
#### It runs every minute and creates a new record in the memory_log table.

#### File Location
- `memory_tracker/memory_tracker/cron/cronjobs`
- `memory_tracker/memory_tracker/cron/tasks.py`
```cron
* * * * * bash /srv/memory_tracker/memory_tracker/cron/run_tasks.sh
```
