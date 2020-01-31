The app collects statistics about its local server and push them to a central server.

Stats of local server can include:
- Delay time of a Postgres' database
- Number of Query in queue of a Postgres' database
- Ram Available
- Load Average


It has two parts:
- **Client**: does regular checking and push stats to a central server
- **Central Server**: receives stats from Clients and stores in redis

Client uses websockets to push data to server.
The stats are stored in redis.


## How to
