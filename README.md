<div align="center">
    <img src="https://raw.githubusercontent.com/Jobsity/ReactChallenge/main/src/assets/jobsity_logo_small.png"/>
</div>

# Flask Challenge

## Description
This project is designed to test your knowledge of back-end web technologies, specifically in the Flask framework, Rest APIs, and decoupled services (microservices).

## Assignment
The goal of this exercise is to create a simple API using Flask to allow users to query [stock quotes](https://www.investopedia.com/terms/s/stockquote.asp).

The project consists of two separate services:
* A user-facing API that will receive requests from registered users asking for quote information.
* An internal stock aggregator service that queries external APIs to retrieve the requested quote information.

For simplicity, both services will share the same dependencies (requirements.txt) and can be run from the same virtualenv, but remember that they are still separate processes.

## Minimum requirements
### API service
* Endpoints in the API service should require authentication (no anonymous requests should be allowed). Each request should be authenticated via Basic Authentication.
You have to implement the code to check the user credentials are correct and put the right decorators around resource methods (check the auth.helpers module).
* When a user makes a request to get a stock quote (calls the stock endpoint in the api service), if a stock is found, it should be saved in the database associated to the user making the request.
* The response returned by the API service should be like this:

  `GET /stock?q=aapl.us`
  ```
    {
    "symbol": "AAPL.US",
    "company_name": "APPLE",
    "quote": 123
    }
  ```
  The quote value should be taken from the `close` field returned by the stock service.
* A user can get his history of queries made to the api service by hitting the history endpoint. The endpoint should return the list of entries saved in the database, showing the latest entries first:
  
  `GET /history`
  ```
  [
      {"date": "2021-04-01T19:20:30Z", "name": "APPLE", "symbol": "AAPL.US", "open": "123.66", "high": 123.66, "low": 122.49, "close": "123"},
      {"date": "2021-03-25T11:10:55Z", "name": "APPLE", "symbol": "AAPL.US", "open": "121.10", "high": 123.66, "low": 122, "close": "122"},
      ...
  ]
  ```
* A super user (and only super users) can hit the stats endpoint, which will return the top 5 most requested stocks:

  `GET /stats`
  ```
  [
      {"stock": "aapl.us", "times_requested": 5},
      {"stock": "msft.us", "times_requested": 2},
      ...
  ]
  ```
* All endpoint responses should be in JSON format.

### Stock service
* Assume this is an internal service, so requests to endpoints in this service don't need to be authenticated.
* When a stock request is received, this service should query an external API to get the stock information. For this challege, use this API: `https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv`.
* Note that `{stock_code}` above is a parameter that should be replaced with the requested stock code.
* You can see a list of available stock codes here: https://stooq.com/t/?i=518

## Architecture
![Architecture Diagram](diagram.svg)
1. A user makes a request asking for Apple's current Stock quote: `GET /stock?q=aapl.us`
2. The API service calls the stock service to retrieve the requested stock information
3. The stock service delegates the call to the external API, parses the response, and returns the information back to the API service.
4. The API service saves the response from the stock service in the database.
5. The data is formatted and returned to the user.

## Bonuses
The following features are optional to implement, but if you do, you'll be ranked higher in our evaluation process.
* Add unit tests for the bot and the main app.
* Connect the two services via RabbitMQ instead of doing http calls.
* Use JWT instead of basic authentication for endpoints.

## How to run the project
The project is available through docker and docker-compose.

Rename the `.flaskenv.example` file into `.flaskenv` in both apps and change any desired variable.

To initialize the project, run the apps and add initial user data:
```
$ make init
```
The command above adds two users available, an admin user `admin:admin` and a regular user `johndoe:john`.
After running the command above, the apps will be available at `localhost:5000` and `localhost:5001` respectively.

To rebuild the docker-compose:
```
$ make build
```

To run in daemon:
```
$ make run
```

Running tests:
```
$ make test-api
$ make test-stock
```

## Development commands
The makefile has two commands available for the database migrations

To generate a new migration based on schema changes:
```
$ make db-migrate msg="Migration message"
```

To upgrade the current database to head:
```
$ make db-upgrade
```

## Issues with testing
Unfortunately it wasn't possible as of now to have a dedicated database for testing purposes, so the current testing uses the generated sqlite database from the main application, and makes use of the initial data from the two inserted users. So make sure to run `make init` before running tests!


## Differences from the base project
The api service now uses JWT authentication, the token generation is available through the `login` endpoint, which is a POST that takes the following JSON body:
```json
{
  "username": "username",
  "password": "password"
}
```

Every other endpoint from the api service now requires a bearer authentication, through a `Bearer {token}` authorization header.

## TO-DOs
* Add decent logging
* Spend even more hours figuring out why this combination of libs make it so hard to use a testing in-memory database
* Add production deployment steps and example environment through gunicorn
* Add RabbitMQ communication between the services
* Add pagination to the history endpoint
* Add swagger or redoc for the api documentation
