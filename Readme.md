
# NetWatch

A simple network utility to periodically TCP test and track a set of targets on a specific port.

Being able to establish and track basic TCP connectivity with a host on a specific port is a common network task. Netwatch is essentially a layer 4 health check. Run the NetWatch application via Docker in the source network (AWS VPC etc) and configure it periodically test TCP connectivity to your targets and record the results. Your targets could be other hosts that are part of the same network or maybe a peer network connected over VPN. Or, your target hosts could be internet-accessible - you can watch google.com on port 443 for example.

### Why is this useful?


Although it can be used for a range of scenarios, the application was designed around a specific use case... The scenario where you have a hub network and many spokes and there is a need for the hub network to continuously generate packets and attempt to reach hosts in the spokes. The spoke networks can then monitor these repeating and predictable packets from NetWatch in the hub and diagnose connectivity issues. In this specific scneario, it's especially useful where the VPN relies on NAT and engineers working on the spoke networks need to establish packets are arriving at the firewall.

But more broadly, NetWatch might help if you find yourself with the need to set up a repeating TCP tester and be in-control of where those packets are coming from.

## Mechanics

There are two main parts to the application. The backend and the client.

### Backend

The backend is written in Python. Among other things, when started the backend will start a series of processes:
- History purge. A process to routinely clear out connection history according to the target's setting.
- Web sessions purge. A process to routinely clear out expired web sessions.
- HTTP endpoint. A process to serve backend API requests for the client.
- Target connection handler. A process to routinely scan for acceptable targets in the database and generate looping daemon processes for each.

### Client

The Client uses the Vue 2 framework. Authentication is handled via HTTP-only cookies and data is retrieved from the backend API - the URL for which is derived from the application root, prefixed with "/api/".

## Installation

NetWatch should be implemented with Docker (https://hub.docker.com/r/tb00/netwatch). The docker image is published so that the backend and client are run on startup, with Nginx acting as both a server for the client static files and a proxy for the backend API.

### Environment Variables

| VAR | REQUIRED | DEFAULT | NOTES |
|---|---|---|---|
| MYSQL_HOST | YES | N/A | MySQL host address |
| MYSQL_DB | YES | N/A | MySQL database name |
| MYSQL_USER | YES | N/A | MySQL user |
| MYSQL_PASSWORD | YES | N/A | MySQL password |
| ROOT_USER | NO | N/A | Root user to create when starting the application |
| ROOT_PASSWORD | NO | N/A | Root user password |
| CORE_LOG_LEVEL | NO | info | Backend (core) application log level |
| HTTP_LOG_LEVEL | NO | info | Client app log level |

1. Provision your MySQL database, with a user that has full control over the database.
2. Provision NetWatch, passing the environment variables as needed.

Example Docker run command:
```
docker run --network local_net0192 --rm -it -p 8080:8080 --name netwatch \
-e MYSQL_HOST=netwatch_mysql \
-e MYSQL_DB=myapp \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=securepassword \
-e ROOT_USER=root \
-e ROOT_PASSWORD=root \
-e CORE_LOG_LEVEL=info \
-e HTTP_LOG_LEVEL=info \
netwatch:beta
```

### Users

The root user is optional. But, at least on first setup, you will need to create the root user to get access and create subsequent users. Once this is done, you could remove the root user in the application and not pass the environment variable on next run to prevent it being recreated. You can also just keep the root user if needed. It is recommended to set a strong root user password and change it periodically.

Currently, all users are administrators and have full control to edit, delete and create other users.

## Usage

### Dashboard

The dashboard shows your targets. From here, you can add more targets, search, filter, delete and drill down in to their history.

#### Add new targets

Select the plus icon next to the search. A popup will show and allow you to set your options:

| Option | Description |
|---|---|
| Name | Friendly target name. This does not need to be unique. |
| Host | Domain or IP to watch (TCP test). |
| Port | Port to watch on the target. |
| Interval | how long to wait in-between probes in seconds. This is also the time to wait before failing the connection (timeout). Although, the timeout will never exceed 60 seconds, even if the interval is set higher. |
| History Retention Period | Combines with History Retention Unit, this determines how long to retain history data for the target. |
| History Retention Unit | Combines with History Retention Period, this determines how long to retain history data for the target. |
| Enabled | Whether the target is enabled or disabled. |

To prevent the database growing too much, be conservative about your history retention values.

### Target History

From the dashboard, select the graph icon for any target you wish to see the history for. If data is available, a graph will populate and indicate whether tests have been successful over a period of time, with 1 denoting success and 0 denoting failure.

Graphs aggregate data, so if you see a data-point somewhere between 1 and 0, it means that during this aggregated period, there have been at least one success and one failure. For example, suppose you are aggregating by 10 seconds. You are testing every 5 seconds. On one test, it succeeded and on the other it failed. For this data-point, the reading would show as 0.5. 

You can set your aggregation (or "group by") at the top right of the page, next to the "run" button.

### Users

Use the Users section to administer your users. Like the dashboard, you can search, filter, delete and create users.

### License & warning
NetWatch is designed and maintained as part of a personal project. The application is is in beta and there is currently no assurance that a production-ready release will be published. Unit tests, vulnerability scanning and refactors would need to happen for this. If you use NetWatch, use it at your own risk and be sure you understand what those risks are. 

Usage of the application is currently free, limited to a non-commercial capacity. Use the tool as an engineering tool, but not directly part of your commercial value proposition. 

#### Development

To aid development, there is a makefile with predefined targets. When developing locally, you can run the following series of commands:

```make dev-mysql``` - to start the MySQL service in docker. This will use an init script to create the database too.
```make dev-backend``` - to start the backend python module.
```make dev-client``` - to run the client with yarn.
```make dev-nginx``` - to run Nginx as a proxy on localhost port 9090 (http://localhost:9090)

Or, you can run ```make dev-compose``` ro run all of these commands and open them all, except MySQL, in terminal sessions.

To publish, again use the makefile and run ```make build``` followed by ```make publish```. You can use ```make docker-up``` after building to production-test the build before publishing. This will start a fresh MySQL container (even if one is already running).