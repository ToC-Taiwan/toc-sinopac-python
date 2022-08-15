# [](https://gitlab.tocraw.com/root/toc-sinopac-python/compare/v0.0.3...v) (2022-08-08)

## CHANGELOG

## [0.0.3](https://gitlab.tocraw.com/root/toc-sinopac-python/compare/v0.0.2...v0.0.3) (2022-08-06)

### Bug Fixes

* **limit:** remove sinopac request limit, upgrade python to 3.10.6 ([9ea9ccb](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9ea9ccb36da46f87d902b11def58b1795fa53558))
* **log:** remove redundant log get worker, limit worker one second to 85 ([cbfa6d4](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/cbfa6d419f517c3857963f89582f39ffa2ca81e5))

### Features

* **fetch:** add every 5 secs, 500 fetch limit ([121ec73](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/121ec73e03e8eb911db8d0c372ceaaefc86815ba))
* **fetch:** change contract to num, modify fetch rate to 95 times per second ([88ed683](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/88ed683c2391a5b52412e6003a036a5673812d6c))
* **limit:** add request limit in env, add request limit in snapshot, ticks, kbars ([d876e23](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/d876e2375d3611f863a0a54426592a906e4e0af9))

## [0.0.2](https://gitlab.tocraw.com/root/toc-sinopac-python/compare/v0.0.1...v0.0.2) (2022-07-21)

### Bug Fixes

* **callback:** fix key error in place order callback ([9524b5b](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9524b5be9179abc05a894f8e216fc771a57c6b0e))
* **ci:** fix stop docker fail at no *.log, update shioaji 0.3.6.dev2 ([73f13f5](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/73f13f5f8dc3c049e209f6e6ec37ecb5eda18080))
* **exception:** remove exception in update status ([cedeccb](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/cedeccbf4dd5db805230a8d5ce8fb22500f0ae83))
* **snapshot:** fix timeout error in snapshot, ignore stock category is 00 ([c016afe](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/c016afe468d206d9369df31c3df3efb5368c695e))
* **status:** add lock in update order status instant ([e7cc709](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/e7cc7096333ead01d8ae077ae3ec460edc22d3e1))

### Features

* **cancel:** add sleep 1 seccond when add times ([4f239fc](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/4f239fcf661fcb4795cb6445e6530a2640909759))
* **workder:** let main worker does not join worker pool ([fac9019](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/fac9019f9de25d297f45d80cfff5583f3f64113e))

## [0.0.1](https://gitlab.tocraw.com/root/toc-sinopac-python/compare/87093d8e2b3be1cdbdd969292775d7e05139a9d5...v0.0.1) (2022-07-07)

### Bug Fixes

* **ci:** add double quote in env variable ([8ad2b05](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/8ad2b05ccbd3f9af47dc22fffc2abd06327f8fed))
* **ci:** add echo file absolute path ([598650c](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/598650caa3aea15062654809f4ff2486e5cd2cad))
* **ci:** add env file in docker run ([cd12982](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/cd129821587074c008d6e81e0e1357978b4bc0dc))
* **ci:** add missing double quote of ssh command ([5d31f6f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/5d31f6f96edec5e344927bbb1dc6ef7318d00c91))
* **ci:** add missing env file by scp ([933a84a](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/933a84a3febee50baf9a65e8144c2ef430798044))
* **ci:** add mkdir before scp command ([e5ef028](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/e5ef0283a012dc460719f9bf6e5cead3b94e2fe9))
* **ci:** fix env variable missing ([1a582aa](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/1a582aa7ce07f9b277997f34d372ddbbff149f87))
* **ci:** fix missing dependency in ci lint ([a8a76c2](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/a8a76c28b0de73637cfb188372dffff78c2862be))
* **ci:** fix scp wrong file name ([a420d6e](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/a420d6e4862f71d47dd04f7bb95a36500a9a485f))
* **ci:** fix wrong env path ([1270a68](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/1270a68f35584c0854289064ef1e6bef89ee269a))
* **ci:** remove comment at yaml multi line ([e068a02](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/e068a022de2a1b3a613452b189a4d7a14ed819f5))
* **ci:** remove redundant colon in docker run command ([c7e1f77](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/c7e1f778271b7d72070e0283dbb7b25c1fe4133e))
* **ci:** temp does not use secret of ci ([db58171](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/db581710f3e4bc63c6900c4a32d85d09c34702c3))
* **close:** fix len of Ticks error ([33aa605](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/33aa6051e0889e0d8b24ba0b12a9c05a7da49d78))
* **close:** fix try except then get zero close ([8b40bf0](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/8b40bf0abcf813c6fb2e91396fc395542ba09d4c))
* **container:** add driver to docker network ([99ff4ae](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/99ff4aec783f42ac79de7282b112fe39485736b4))
* **container:** change env name to avoid docker host wrong ([80ed1db](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/80ed1db72221ab5af227a8361b6c72db56b02a10))
* **container:** fix missing encoding in bytes ([f29c8a3](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/f29c8a3d8f536fd80bce9c6ab4cdb6c17026f58a))
* **container:** fix the way use docker network ([0aa116f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/0aa116f6e1aa462f5ac6e158cc1bfe20cb0dc618))
* **grpc:** add queue full to avoid memory leak after client disconnect ([830c98e](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/830c98e06b585969a417b2453163b785b6892aba))
* **grpc:** fix wrong augument in new server ([3b264d3](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/3b264d313cd3bdab9b88cea3e58d452dbec210f7))
* **heartbeat:** change the send heartbeat method to fix pika publish error ([71167c1](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/71167c131818468509730d97a9371a74edd3536e))
* **heartbeat:** fix debug has no initial ([9bbafae](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9bbafae4c88f45d731d2ffa6bc4b5f958f014192))
* **proto:** fix wrong compile proto script ([45210e2](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/45210e203c0daa3e8224002939c741d01e24d01c))
* **rabbitmq:** add process data to send heartbeat to avoid disconnect from rabbitmq ([1add815](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/1add815f16c4b680a6bbf9fec2ce2edc755a7d64))
* **rabbitmq:** fix wrong delete exchange status code ([8b9884d](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/8b9884deb6fac959458f806352cf27ba6645b162))
* **shioaji:** add missing sleep in login fail ([f8cdd69](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/f8cdd69a8d01d1113312d90d3fedb9a6bcbde8f9))
* **simulation:** fix wrong logic in simulation buy ([a9d529b](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/a9d529b3865691aae009ec82713c50e3fd602e90))
* **simulation:** key error when simulation trade in map of order count ([0248670](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/02486705c9b1ba90333018ba0a7f0fb42889b91e))

### Features

* **channel:** add all stream channel, sinopac trade method ([cb37927](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/cb379270f30a30667528bc1b2e10f2d233bb9070))
* **channel:** change data channel from rpc to rabbit mq ([68a9864](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/68a98648c5178c1b885f0ed3adec707b101e5d44))
* **close:** add check length of last count ([ccf122f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/ccf122ff1a9d4ec8213a9afc0c30e4c961dd39cf))
* **close:** add sinopac api try get last count ([558926e](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/558926e329bbc24783527d7c300eb89a149e8086))
* **container:** add docker package to start rabbitmq container self ([8ef4288](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/8ef42888090858305387b99894450f2e880e6071))
* **container:** add except timeout error when terminate rabbitmq ([22ea974](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/22ea9749beabc3e24219eb7b45dd1689740ba879))
* **container:** add try except to request check health ([b9bffd2](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/b9bffd232d0cdac3018b6f85453c1919e1a637c3))
* **container:** change deployment network to host ([0dbfc0a](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/0dbfc0af93e36bef55ada6125586eed05f8d8077))
* **container:** change network mode to host ([fa415a1](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/fa415a11dee2f8345b2bbfd8df1ef3c1181cac0c))
* **container:** use rabbit api health check to check container is started ([4d8d313](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/4d8d3135cb38ac746df9b5ad8b0318fd12511f1f))
* **exception:** add try except in shioaji login to avoid login fail stuck ([296fc84](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/296fc8462cfa5f419338671cd20829965a3bf7e2))
* **grpc:** add stream callback, remove queue block ([ef6f839](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/ef6f8391205c16802b153edb6743e268c62dc95b))
* **grpc:** add stream event to client, move sinopac callback to grpc, and set in workers ([654e64f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/654e64fa8421ebb29522fa7a9355327f5bbb1019))
* **grpc:** increase max message size to 1024*1024*1024 ([542d581](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/542d581263f5f2a1867fd8a3ac3b3ccf7b57689c))
* **health:** split grpc servicer, add debug mode for machine trading ([16e194d](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/16e194dcb27e6fa490c3a63decedfb0937ac343f))
* **heartbeat:** add heartbeat to detect client healthy, remove server token ([ca97035](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/ca97035089407106bbbaa912d15690739275cf4e))
* **history:** add history kbar, close ([2b16bdd](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/2b16bdd2b43f47702a6d4557946d784ba5a193e7))
* **history:** add History Tick rpc ([60acb68](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/60acb6858f7920446689b483622772b68ec292bc))
* **layout:** add grpc and sinpac class alpha ([87093d8](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/87093d8e2b3be1cdbdd969292775d7e05139a9d5))
* **layout:** let all file in same module, add load .env ([389582f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/389582fb14974fe44ab53283fadbf3969d3990ad))
* **login:** extend system maintenance wait time to 75 sec ([5d46f6d](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/5d46f6d23d5312b662c393a504b6aa53000931b7))
* **login:** remove check need fetch, update shioaji to 0.3.6.dev1 ([3b3dd4d](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/3b3dd4d1963191537d35b69df1d71dfb25e60004))
* **performance:** add sinopac worker class to get best connection ([9f85f48](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9f85f488d0d1f1ebf028e7a050a7551e337b9cf7))
* **python:** upgrade to 3.10, fix new pylint warning ([31607fb](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/31607fb0dbe8ef8f895836a655e056fd194f9ebb))
* **rabbitmq:** deprecate run rabbitmq conatiner, put it into ci, only reset exchange in startup ([73226b3](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/73226b30f073d276f6041a7f4af0d77acc11a33c))
* **secret:** add rabbit container secret to env file ([52312b4](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/52312b48ab001098b9b993daf0d002e66947f089))
* **shioaji:** revert to 0.3.5.dev1 ([5184c34](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/5184c3408352268fd9c8e4b03db0bdcc9cbf4cd7))
* **shioaji:** update ver to 0.3.6.dev0 ([9fd86ac](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9fd86ac30f9f7660b1f65e3033798696d9f8dbf6))
* **sinopac:** add constant, add main worker, add fill local stock list, order status ([1b4f528](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/1b4f5287a7325785f6a346aa064a65e4934a06e2))
* **sinopac:** finish multi login ([351b095](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/351b09511ea028d15275326526d613b39c2a8fba))
* **snapshot:** add snapshot by stock, multi threading of connection alpha ([608b5cd](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/608b5cd5d174200ec9d63d6b3ae59f01012d8bc1))
* **stock:** add rpc GetAllStockDetail method ([4ad1d94](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/4ad1d94e31f52e8f0bfbfbe99f94ccd660d59639))
* **subscribe:** add subscribe unscribe tick, bidask, add volume rank ([e763778](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/e76377843d4fba7e10bc57672f506fad9f4fd911))
* **subscribe:** add unsubscribe all, add last sucess fetch file ([a46bf97](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/a46bf97b97affd9fddfc57a5ac0c70d88a933de1))
* **thread:** change get history tick to multi threads ([bf09445](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/bf09445d62c05b5206348cfeb36b4a76967f8ff5))
* **timeout:** add timeout check in ticks, kbar ([987ce14](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/987ce14d7e7c690af90d69045a54d4253a3d0b98))
* **trade:** add trade service, schedule exit, env class, move project layout ([5ef42ad](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/5ef42adfd008c37bd47df9a70da6fea7b93229ff))
* **tse:** change GetStockSnapshotTSE return single message ([f9ed67b](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/f9ed67b53b2845cf3358408b893291eee80974ea))
