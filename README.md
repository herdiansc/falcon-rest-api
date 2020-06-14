# Falcon REST API
This is an ecample project of a rest api server built with falcon.

## Features
- Contains 2 resources: users and clothes
- Contains CRUD for each resource
- Demontrates simple authentication using JWT
- [EXPERIMENTAL] Demontrates upload image
- Acceptance test
- [TBD] Unit test
- Docker containerization

## How to Run
Run this project using docker:
- `docker-compose up --build` to build the project
- `docker-compose start` to start the project
- access `http://localhost:9000/[resource]` where `resource` is either `users|clothes`

## Example request
- Uses jwt token, here is an example of a valid jwt token: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8`
- Get users: `curl -XGET -H "Content-type: application/json;" -H "Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8" 'http://localhost:9000/users'`
- Add clothe: `curl -XPOST -H "Content-type: application/json" -H "Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8" -d '{"name":"herdian","email":"herdian@mail.com","size":"S"}' 'http://localhost:9000/clothes'`

# Running Tests
- Go to project root directory
- Run `py.test app/tests/ -vv`
- Screenshot of the test result:
![test result](https://raw.githubusercontent.com/herdiansc/falcon-rest-api/master/screenshots/test_result.png "test result")
