# CHANGELOG

<a name="v1.2.0"></a>

## [v1.2.0](https://github.com/ToC-Taiwan/toc-machine-trading/compare/v1.1.0...v1.2.0)

> 2022-12-10

### Chore

* **comment:** remove all redundant comment, modify order callback log
* **dependency:** update dependency, modify compile proto script
* **log:** modify sinopac login callback message
* **protobuf:** change to official google proto package
* **readme:** modify readme, add make file, update dependencis
* **sinopac:** make sinopac naming, import, arrange make sense

### Feat

* **grpc:** add otc kbar, use threading to increase speed of get order from mq
* **lock:** add lock for GetOrderStatusArrFromMQ
* **log:** add color in logger module
* **logger:** modify log format, remove redundant constant
* **monitor:** add prometheus client and listen 8887
* **mq:** add send order arr to mq
* **order:** increase efficency of send order to mq
* **order:** add update order status when place order cb
* **proto:** update latest toc trade protobuf
* **simulator:** split simulate trade from sinpac to a single simulate class

### Fix

* **ci:** fix missing lint script
* **lint:** fix R1714: Consider merging these comparisons with 'in'
* **lock:** add missing lock for get local orders, remove clear local order method
* **log:** fix wrong message in place order callback, lower all log
* **order:** move update status into lock, split simulate and prod order get method
* **order:** add update order status for main sinopac worker after login
* **order:** fix place order callback cannot has name from local contract
* **timeout:** fix snapshots, position timeout cause exception

### Refactor

* **login:** modify sinopac login message

### Revert

* **log:** due to user root, no color, revert to console logger

<a name="v1.1.0"></a>

## [v1.1.0](https://github.com/ToC-Taiwan/toc-machine-trading/compare/v1.0.0...v1.1.0)

> 2022-12-02

### Chore

* **changelog:** modify changelog for v1.0.0
* **dependency:** update shioaji to 0.3.6.dev6, grpc tool version
* **log:** add shioaji version in start up
* **logger:** modifiy login message, add stock in unsubscribe bidask
* **naming:** refactor all naming to distinguish stock and future

### Ci

* **actions:** remove delete deployment and productoin env
* **container:** move registry from docker hub to github
* **deployment:** run specific image tag instead of latest, catch yahoo finance key error
* **docker:** add git hash for docker build tag

### Feat

* **debug:** add unsubscribe all tick and bidask when machine trading miss heartbeat in debug mode
* **dependency:** update shioaji to 0.3.6.dev7
* **log:** change all log extention to .log and modify reademe
* **mypy:** add check-untyped-defs and fix, update python 3.10.8
* **order:** change get simulate arr to send by mq
* **position:** add get future postion grpc method
* **quantity:** if deal not equal to original, use deal otherwise use order
* **simulate:** add clear local order list in dev mode
* **simulation:** reduce future simulation trade finish time to 1 sec
* **sinopac:** add sleep 60 sec, if sinopac login timeout
* **snapshot:** add GetStockSnapshotOTC rpc
* **stream:** add stream data from yahoo finance for grpc
* **yahoo:** add previousClose to yahoo finance price
* **yahoo:** add retry fetch if no data return

### Fix

* **grpc:** fix wrong return of rpc method
* **grpc:** catch runtime error when serve grpc
* **heartbeat:** fix unsubscribe at wrong time
* **heartbeat:** fix debug prod mode in the same time does not terminate, add clear simulation order
* **lint:** fix lint error
* **lint:** fix lint Unnecessary "else" after "return"
* **lint:** fix Redefining built-in request connection error
* **lint:** fix lint error
* **lint:** fix missing return of list position
* **login:** fix wrong loging status in sinopac login callback
* **login:** catch sinopac login timeout error
* **login:** fix value error in sinopac login
* **order:** fix filled order quntity to deal quntity
* **position:** catch list position error
* **quantity:** deal quantity should compare to order qty not status qty
* **type:** fix wrong yahoo finace catch error return type
* **yahoo:** add missing catch urllib3 Protocol error
* **yahoo:** add check key exist
* **yahoo:** check regularMarketPrice and previousClose is None or not
* **yahoo:** fix yf.Ticker raise JsonDecode error
* **yahoo:** add catch RemoteDisconnected and ConnectionError in yahoo finance
* **yahoo:** add catch ConnectionResetError error
* **yahoo:** add catch KeyError in yahoo finance

<a name="v1.0.0"></a>

## [v1.0.0](https://github.com/ToC-Taiwan/toc-machine-trading/compare/v0.0.3...v1.0.0)

> 2022-10-19

### Chore

* **badge:** remove self host gitlab badge
* **ca:** update ca and change password
* **cron:** modify afternoon terminate time to 14:40, disable auto deployment
* **deployment:** remove gitlab k8s agent

### Ci

* **action:** add lint, build to github actions
* **actions:** add workflow_dispatch in workflow condition
* **actions:** add checkout, on main to actions
* **agent:** add k8s agent for gitlab
* **deployment:** add deployment temp to github action
* **deployment:** complete whole deployment flow
* **env:** move export PYTHONPATH before mypy
* **env:** add missing PYTHONPATH
* **migrate:** delete gitlab ci, add reset environment before deployment
* **port:** add machine port in actions
* **python:** fix python version in actions lint
* **runner:** change lable which runner need
* **runner:** change self host runner to cloud runner
* **script:** use script to lint instead

### Feat

* **actions:** add deactivate environment in actions
* **actions:** add stop deployment to actions
* **ci:** add needs lint to build
* **container:** change python base container
* **cron:** remove 1:20 terminate
* **dependency:** update shiaoji to 0.3.6.dev4 and other dependency
* **docker:** change base to python slim
* **future:** add simulate trade future, modifiy protobuf
* **future:** finish all trade of future, history data of future, modify place order cb for future
* **future:** add future detail, add subscribe future tick
* **future:** add fimtx snapshot, modifiy event callback before use rabbitmq
* **log:** modify order callback log, add exit if reconnect in login
* **logger:** add log format in env file
* **protobuf:** use new format of toc trade protobuf
* **shiaoji:** upgrade to 0.3.6.dev3
* **subscribe:** add subscribe future bidask

### Fix

* **actions:** merge deployment to one action file
* **actions:** remove dependency in stop deployment
* **actions:** remove redundant double quote in mkdir of env
* **actions:** fix wrong image name for deployment
* **actions:** remove redundant command
* **actions:** add quote to sinopac env secrets
* **actions:** add PYLINTHOME to lint in action
* **build:** fix docker build fail
* **callback:** add missing future bidask callback set
* **commit:** add missing commit file
* **deployment:** change runner lable in actions
* **docker:** add missing copy file to image
* **proto:** fix wrong type of suspend and simtrade
* **protobuf:** modify proto file import way
* **pylint:** add no-menber disable, recompile protobuf
* **recursive:** fix kbar, ticks, close recursive arguments wrong
* **request:** add missing timeout in request
* **simulation:** fix future code does not initial in current count map
* **unsubscribe:** add unsubscribe future bidask in unsubscribe_all_bidask

<a name="v0.0.3"></a>

## [v0.0.3](https://github.com/ToC-Taiwan/toc-machine-trading/compare/v0.0.2...v0.0.3)

> 2022-08-06

### Feat

* **fetch:** change contract to num, modify fetch rate to 95 times per second
* **fetch:** add every 5 secs, 500 fetch limit
* **limit:** add request limit in env, add request limit in snapshot, ticks, kbars

### Fix

* **limit:** remove sinopac request limit, upgrade python to 3.10.6
* **log:** remove redundant log get worker, limit worker one second to 85

<a name="v0.0.2"></a>

## [v0.0.2](https://github.com/ToC-Taiwan/toc-machine-trading/compare/v0.0.1...v0.0.2)

> 2022-07-22

### Feat

* **cancel:** add sleep 1 seccond when add times
* **workder:** let main worker does not join worker pool

### Fix

* **callback:** fix key error in place order callback
* **ci:** fix stop docker fail at no *.log, update shioaji 0.3.6.dev2
* **exception:** remove exception in update status
* **snapshot:** fix timeout error in snapshot, ignore stock category is 00
* **status:** add lock in update order status instant

<a name="v0.0.1"></a>

## v0.0.1

> 2022-07-07

### Chore

* **basic:** add python basic file
* **changelog:** add changelog
* **dependency:** correct misspell, update dependency, modify env example
* **hook:** add hook for pre-commit, modify requirements
* **logger:** remove log in channel down callback
* **package:** remove docker in rabbitmq setting
* **proto:** fix wrong proto naming, change deploy to manual
* **proto:** modify protobuf method sort
* **proto:** update compile proto script
* **protobuf:** rename proto and rpc
* **rabbitmq:** change order_status routing key to order
* **readme:** update run command
* **readme:** modify python version, launch command

### Ci

* **ci:** add ci/cd file, Dockerfile
* **commit:** add custom script to pre-commit
* **commit:** add standart pre-commit
* **container:** add stop toc-rabbitmq in ci script
* **docker:** add docker sock to run command

### Feat

* **channel:** add all stream channel, sinopac trade method
* **channel:** change data channel from rpc to rabbit mq
* **close:** add check length of last count
* **close:** add sinopac api try get last count
* **container:** add docker package to start rabbitmq container self
* **container:** change deployment network to host
* **container:** add except timeout error when terminate rabbitmq
* **container:** change network mode to host
* **container:** add try except to request check health
* **container:** use rabbit api health check to check container is started
* **exception:** add try except in shioaji login to avoid login fail stuck
* **grpc:** add stream event to client, move sinopac callback to grpc, and set in workers
* **grpc:** add stream callback, remove queue block
* **grpc:** increase max message size to 1024*1024*1024
* **health:** split grpc servicer, add debug mode for machine trading
* **heartbeat:** add heartbeat to detect client healthy, remove server token
* **history:** add history kbar, close
* **history:** add History Tick rpc
* **layout:** add grpc and sinpac class alpha
* **layout:** let all file in same module, add load .env
* **login:** extend system maintenance wait time to 75 sec
* **login:** remove check need fetch, update shioaji to 0.3.6.dev1
* **performance:** add sinopac worker class to get best connection
* **python:** upgrade to 3.10, fix new pylint warning
* **rabbitmq:** deprecate run rabbitmq conatiner, put it into ci, only reset exchange in startup
* **secret:** add rabbit container secret to env file
* **shioaji:** update ver to 0.3.6.dev0
* **shioaji:** revert to 0.3.5.dev1
* **sinopac:** finish multi login
* **sinopac:** add constant, add main worker, add fill local stock list, order status
* **snapshot:** add snapshot by stock, multi threading of connection alpha
* **stock:** add rpc GetAllStockDetail method
* **subscribe:** add subscribe unscribe tick, bidask, add volume rank
* **subscribe:** add unsubscribe all, add last sucess fetch file
* **thread:** change get history tick to multi threads
* **timeout:** add timeout check in ticks, kbar
* **trade:** add trade service, schedule exit, env class, move project layout
* **tse:** change GetStockSnapshotTSE return single message

### Fix

* **ci:** fix env variable missing
* **ci:** add double quote in env variable
* **ci:** fix wrong env path
* **ci:** add missing double quote of ssh command
* **ci:** temp does not use secret of ci
* **ci:** remove comment at yaml multi line
* **ci:** fix missing dependency in ci lint
* **ci:** add env file in docker run
* **ci:** remove redundant colon in docker run command
* **ci:** add mkdir before scp command
* **ci:** add missing env file by scp
* **ci:** fix scp wrong file name
* **ci:** add echo file absolute path
* **close:** fix len of Ticks error
* **close:** fix try except then get zero close
* **container:** add driver to docker network
* **container:** fix the way use docker network
* **container:** change env name to avoid docker host wrong
* **container:** fix missing encoding in bytes
* **grpc:** add queue full to avoid memory leak after client disconnect
* **grpc:** fix wrong augument in new server
* **heartbeat:** change the send heartbeat method to fix pika publish error
* **heartbeat:** fix debug has no initial
* **proto:** fix wrong compile proto script
* **rabbitmq:** fix wrong delete exchange status code
* **rabbitmq:** add process data to send heartbeat to avoid disconnect from rabbitmq
* **shioaji:** add missing sleep in login fail
* **simulation:** fix wrong logic in simulation buy
* **simulation:** key error when simulation trade in map of order count

### Style

* **black:** add black as formatter and add to pre-commit
