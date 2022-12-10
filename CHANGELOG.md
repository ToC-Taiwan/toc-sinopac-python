# [](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v1.2.0...v) (2022-12-10)

## CHANGELOG

# [1.2.0](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v1.1.0...v1.2.0) (2022-12-09)

### Bug Fixes

* **ci:** fix missing lint script ([ad633c5](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ad633c57c65e0e91aa10cfd18ffa80e6b13f33a4))
* **lint:** fix R1714: Consider merging these comparisons with 'in' ([09caf67](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/09caf675b252343417a725f31616a524df597dd0))
* **lock:** add missing lock for get local orders, remove clear local order method ([88d1afd](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/88d1afd4997f90e308920cc56dd1657b388a275a))
* **log:** fix wrong message in place order callback, lower all log ([647ed9d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/647ed9d5ebebcef6e93ae0dd5cffd2f9e69c2c40))
* **order:** add update order status for main sinopac worker after login ([a8278ce](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a8278ce6240fe19cae2a278960985240f82d8d35))
* **order:** fix place order callback cannot has name from local contract ([8dfac5e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8dfac5ef38251e288d92383b9e35cbacf4804480))
* **order:** move update status into lock, split simulate and prod order get method ([9462f36](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9462f362725124ca14477afa0090132a844a0096))
* **timeout:** fix snapshots, position timeout cause exception ([eea82fa](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/eea82fa52710d7baf1f014f509abb579fc64515e))

### Features

* **grpc:** add otc kbar, use threading to increase speed of get order from mq ([6a754ca](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/6a754ca38cae2055d62515f837793947a7a3dd01))
* **lock:** add lock for GetOrderStatusArrFromMQ ([c7e09bf](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/c7e09bf1505c5a0232ae06657be2f2ddf2147463))
* **log:** add color in logger module ([a81b4fe](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a81b4fe07d80aa04ca54fe51672c71d62f3a11d8))
* **logger:** modify log format, remove redundant constant ([f8660a4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/f8660a4d3786b08913afef3dabebadd04931da8b))
* **monitor:** add prometheus client and listen 8887 ([159418a](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/159418ae0ce763c207fa077da99fb23609141eca))
* **mq:** add send order arr to mq ([5db2377](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5db23778b9d9d9f64b4d0227e6fad4dae5cc1317))
* **order:** add update order status when place order cb ([a723e5c](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a723e5c6a1388db1c74e16446fe4cad8fd00d273))
* **order:** increase efficency of send order to mq ([77d174c](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/77d174cefc382f4b9e1eaa6cd3be172991907a95))
* **proto:** update latest toc trade protobuf ([1354dca](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1354dca0288fa4682acf2ee6faca39bced15d648))
* **simulator:** split simulate trade from sinpac to a single simulate class ([8825148](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/88251482e1bf9c0ddea814f4adca2ff68a102963))

### Reverts

* **log:** due to user root, no color, revert to console logger ([d1ba769](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d1ba769770f007dc154d8d66a9d8aa66600cb40f))

# [1.1.0](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v1.0.0...v1.1.0) (2022-12-01)

### Bug Fixes

* **grpc:** catch runtime error when serve grpc ([29e53c9](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/29e53c92b8390d4628bc73b841e540edcb09408d))
* **grpc:** fix wrong return of rpc method ([e1cef8f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e1cef8f2c09cfd725318237ba0f14810207249c9))
* **heartbeat:** fix debug prod mode in the same time does not terminate, add clear simulation order ([0222c0d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/0222c0d16acc2b5fa29853612f174dea4140c853))
* **heartbeat:** fix unsubscribe at wrong time ([22ff825](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/22ff825b9b615c7579d2429001ad3b2d6627dc8d))
* **lint:** fix lint error ([59713ae](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/59713ae13a63441b706ee22ede178155b862d627))
* **lint:** fix lint error ([52e795d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/52e795d91eb79254f654389743ed8a407722198a))
* **lint:** fix lint Unnecessary "else" after "return" ([9717265](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/97172654d3100a947f910d555239587ce57e7c77))
* **lint:** fix missing return of list position ([ef543fa](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ef543faeed6625419ebdb7522cd8fe02e381a375))
* **lint:** fix Redefining built-in request connection error ([83cbfc2](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/83cbfc23261fb77d84c37e5b6f066990cfe77251))
* **login:** catch sinopac login timeout error ([e925848](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e925848379df2095759c652de007fc35cbbb6b98))
* **login:** fix value error in sinopac login ([3d024d4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/3d024d42c8aa7f79e2fcac7a90e56a8590dd9d0e))
* **login:** fix wrong loging status in sinopac login callback ([8648b66](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8648b66e7504f2c69e546a8cf1b07b33a8af71c5))
* **order:** fix filled order quntity to deal quntity ([d538d4e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d538d4e949bc62cc44608118b48b62a94da978ff))
* **position:** catch list position error ([693ea9c](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/693ea9cf28235aaae7d9bbfdad79530c545a4c8a))
* **quantity:** deal quantity should compare to order qty not status qty ([e144bbe](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e144bbe5b4e17d969d8a7406cfe7b31e7274d0e1))
* **type:** fix wrong yahoo finace catch error return type ([bb869a4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/bb869a4e64da7448321162a9199dd93760fea8a1))
* **yahoo:** add catch ConnectionResetError error ([c5c8024](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/c5c8024f2ddac2267e1f773e4cc47d7c7dc1cdef))
* **yahoo:** add catch KeyError in yahoo finance ([46554f0](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/46554f0bf185cbb1df67d575730670e812d2b37c))
* **yahoo:** add catch RemoteDisconnected and ConnectionError in yahoo finance ([ce7eb30](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ce7eb30640dfdd562471f8c7601eac72f2cc902a))
* **yahoo:** add check key exist ([2a3953d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/2a3953db59c5f31728ea371d2096e396a513ae56))
* **yahoo:** add missing catch urllib3 Protocol error ([85a8907](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/85a890717d1673f602d52fe69ef16eb25326a0f0))
* **yahoo:** check regularMarketPrice and previousClose is None or not ([5aa87f9](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5aa87f9f653854516db1a950847424d711486d17))
* **yahoo:** fix yf.Ticker raise JsonDecode error ([e4240bf](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e4240bfd6604fd7aaff92e8328371d881ba43149))

### Features

* **debug:** add unsubscribe all tick and bidask when machine trading miss heartbeat in debug mode ([34404dc](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/34404dc6afccf4b20329eb008de2d68a38bb40a3))
* **dependency:** update shioaji to 0.3.6.dev7 ([b5a798d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/b5a798d2876efa730ab66035100f43b52c73b946))
* **log:** change all log extention to .log and modify reademe ([9f6c214](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9f6c214047724d31e57e207f287863d59c9dcbab))
* **mypy:** add check-untyped-defs and fix, update python 3.10.8 ([17abd2a](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/17abd2a49ae8e9c6db906516e87d8c1ac932087b))
* **order:** change get simulate arr to send by mq ([d3d4e45](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d3d4e45aa4d2c0b21d104dcfef98284b074bb60e))
* **position:** add get future postion grpc method ([429b2c0](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/429b2c015cbee5c92a9433985e3956a985ab5b00))
* **quantity:** if deal not equal to original, use deal otherwise use order ([88a3ca1](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/88a3ca1bd065b0b50467387920ee8aa9619daa42))
* **simulate:** add clear local order list in dev mode ([2bb1cda](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/2bb1cda3a0cd4977c0ffa947bfb53736ad447050))
* **simulation:** reduce future simulation trade finish time to 1 sec ([b23f040](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/b23f0407d4af93463281acad2c6131d55a0d20d8))
* **sinopac:** add sleep 60 sec, if sinopac login timeout ([625a3a4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/625a3a43e7b01bc3c53753c22a4c87e71d61d426))
* **snapshot:** add GetStockSnapshotOTC rpc ([d572a22](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d572a220c958ce5f591c10f9c8b2d89ea47d15b2))
* **stream:** add stream data from yahoo finance for grpc ([9299737](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/92997377a510223f771ff3483e0426a11580dcbf))
* **yahoo:** add previousClose to yahoo finance price ([63d9152](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/63d9152841af2a88b76fd8f84ca387c161443da2))
* **yahoo:** add retry fetch if no data return ([5beb142](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5beb142a1a2d09e6c7040fa07fe04a150d319e6b))

# [1.0.0](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v0.0.3...v1.0.0) (2022-10-18)

### Bug Fixes

* **actions:** add PYLINTHOME to lint in action ([505b436](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/505b436bc24c3271da43bf9d11e89b9f9693e566))
* **actions:** add quote to sinopac env secrets ([6ec0c71](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/6ec0c71d0ecf2a1593f7487c70ba1da064fd2fc7))
* **actions:** fix wrong image name for deployment ([d5f4780](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d5f47808e4a3f56aa94bbd01a6b9ba5e4e941cab))
* **actions:** merge deployment to one action file ([5a2daf0](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5a2daf07e9351d2d673f47cfc2d7e297854ef967))
* **actions:** remove dependency in stop deployment ([c91c692](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/c91c692f551f9009ccbe95a8b14ab1ea32a564a3))
* **actions:** remove redundant command ([4240e0b](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/4240e0b79ff40449416f7cffa58d3ad78db225dc))
* **actions:** remove redundant double quote in mkdir of env ([23f5c8f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/23f5c8fe07291f5884a160f50d6b2ed2607a2e1d))
* **build:** fix docker build fail ([f06c6d8](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/f06c6d8abf519b9fb1d196251334e90bfe22b90d))
* **callback:** add missing future bidask callback set ([363cf25](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/363cf259ec99aaea1afc19fa1afd1855a96201f3))
* **commit:** add missing commit file ([2140e8d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/2140e8da61b758c9175911c9d42412f309751a05))
* **deployment:** change runner lable in actions ([a1f5869](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a1f5869022206df8730f5807082d1ae3075f4a80))
* **docker:** add missing copy file to image ([177a6fa](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/177a6face128cdd9c9e3f5a4c86c1e0e19338cc4))
* **protobuf:** modify proto file import way ([cf575bc](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cf575bc70f8696e2ddac23b62b246bfaec996e87))
* **proto:** fix wrong type of suspend and simtrade ([b8df4e6](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/b8df4e6e92bb8cdecc749bc8ecc523a013ff1c20))
* **pylint:** add no-menber disable, recompile protobuf ([0709282](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/0709282e2c64cff6e1e1e8ea82a6973054262472))
* **recursive:** fix kbar, ticks, close recursive arguments wrong ([df9ff43](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/df9ff43b0312ea392047102abae3d9bea7637361))
* **request:** add missing timeout in request ([ae99a6e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ae99a6e242709ee98a5d4d8b5f184acd227185e1))
* **simulation:** fix future code does not initial in current count map ([01047ad](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/01047ad4c8a4dcb2529cd69fe264ada9dfe6b9d2))
* **unsubscribe:** add unsubscribe future bidask in unsubscribe_all_bidask ([843a072](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/843a07261db4cac539b75bfc83805aa53ee8887f))

### Features

* **actions:** add deactivate environment in actions ([058bd5a](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/058bd5a93062628d6faff43ef21caa0b9a791968))
* **actions:** add stop deployment to actions ([7004ccf](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/7004ccf04e8c563ee300a7d0da6ad9b660bede02))
* **ci:** add needs lint to build ([e1eef50](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e1eef50b46f0561fc097254f3ac95133a03c8ed0))
* **container:** change python base container ([cf751fd](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cf751fd38d3589c510d1f163d1a7491f3cbbe658))
* **cron:** remove 1:20 terminate ([59f609f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/59f609f2c128cc1b841b49c7225d7dbc40e5b012))
* **dependency:** update shiaoji to 0.3.6.dev4 and other dependency ([ed73818](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ed73818f883c4d23c4875a577befcbc3a90d8d7c))
* **docker:** change base to python slim ([8b36ec7](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8b36ec7c07d0167d2c98db815cc77ccbccbccfae))
* **future:** add fimtx snapshot, modifiy event callback before use rabbitmq ([9f82356](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9f82356c437c7bfd7dcfd0ece0ddbfd15611ce8d))
* **future:** add future detail, add subscribe future tick ([87f18d1](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/87f18d1f0d6b05f747cb8bb8e5018e8b07d22f7d))
* **future:** add simulate trade future, modifiy protobuf ([d252d29](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d252d29a12aab9f431cf3d3f9d450c189846e826))
* **future:** finish all trade of future, history data of future, modify place order cb for future ([e2408e4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e2408e45df3ba843ce3c49bd45ba936eb66c8a40))
* **logger:** add log format in env file ([fb7a1e5](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/fb7a1e597e7f00ab1972727f0a090c5ba421222d))
* **log:** modify order callback log, add exit if reconnect in login ([1a5aa1d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1a5aa1d2a4a275d2e8c267fa5f7f929c67b1d557))
* **protobuf:** use new format of toc trade protobuf ([b85bd04](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/b85bd04662fb043c5213db3ff7147a6b54452322))
* **shiaoji:** upgrade to 0.3.6.dev3 ([2baf611](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/2baf611be2ec4e7b4adbb4da3338f4bd4bccbd9f))
* **subscribe:** add subscribe future bidask ([16e3c2d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/16e3c2df12f9679d12fa03ca0100512ca7534b76))

## [0.0.3](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v0.0.2...v0.0.3) (2022-08-06)

### Bug Fixes

* **limit:** remove sinopac request limit, upgrade python to 3.10.6 ([9ea9ccb](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9ea9ccb36da46f87d902b11def58b1795fa53558))
* **log:** remove redundant log get worker, limit worker one second to 85 ([cbfa6d4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cbfa6d419f517c3857963f89582f39ffa2ca81e5))

### Features

* **fetch:** add every 5 secs, 500 fetch limit ([121ec73](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/121ec73e03e8eb911db8d0c372ceaaefc86815ba))
* **fetch:** change contract to num, modify fetch rate to 95 times per second ([88ed683](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/88ed683c2391a5b52412e6003a036a5673812d6c))
* **limit:** add request limit in env, add request limit in snapshot, ticks, kbars ([d876e23](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/d876e2375d3611f863a0a54426592a906e4e0af9))

## [0.0.2](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/v0.0.1...v0.0.2) (2022-07-21)

### Bug Fixes

* **callback:** fix key error in place order callback ([9524b5b](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9524b5be9179abc05a894f8e216fc771a57c6b0e))
* **ci:** fix stop docker fail at no *.log, update shioaji 0.3.6.dev2 ([73f13f5](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/73f13f5f8dc3c049e209f6e6ec37ecb5eda18080))
* **exception:** remove exception in update status ([cedeccb](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cedeccbf4dd5db805230a8d5ce8fb22500f0ae83))
* **snapshot:** fix timeout error in snapshot, ignore stock category is 00 ([c016afe](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/c016afe468d206d9369df31c3df3efb5368c695e))
* **status:** add lock in update order status instant ([e7cc709](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e7cc7096333ead01d8ae077ae3ec460edc22d3e1))

### Features

* **cancel:** add sleep 1 seccond when add times ([4f239fc](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/4f239fcf661fcb4795cb6445e6530a2640909759))
* **workder:** let main worker does not join worker pool ([fac9019](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/fac9019f9de25d297f45d80cfff5583f3f64113e))

## [0.0.1](https://github.com/ToC-Taiwan/toc-sinopac-python/compare/87093d8e2b3be1cdbdd969292775d7e05139a9d5...v0.0.1) (2022-07-07)

### Bug Fixes

* **ci:** add double quote in env variable ([8ad2b05](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8ad2b05ccbd3f9af47dc22fffc2abd06327f8fed))
* **ci:** add echo file absolute path ([598650c](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/598650caa3aea15062654809f4ff2486e5cd2cad))
* **ci:** add env file in docker run ([cd12982](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cd129821587074c008d6e81e0e1357978b4bc0dc))
* **ci:** add missing double quote of ssh command ([5d31f6f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5d31f6f96edec5e344927bbb1dc6ef7318d00c91))
* **ci:** add missing env file by scp ([933a84a](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/933a84a3febee50baf9a65e8144c2ef430798044))
* **ci:** add mkdir before scp command ([e5ef028](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e5ef0283a012dc460719f9bf6e5cead3b94e2fe9))
* **ci:** fix env variable missing ([1a582aa](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1a582aa7ce07f9b277997f34d372ddbbff149f87))
* **ci:** fix missing dependency in ci lint ([a8a76c2](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a8a76c28b0de73637cfb188372dffff78c2862be))
* **ci:** fix scp wrong file name ([a420d6e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a420d6e4862f71d47dd04f7bb95a36500a9a485f))
* **ci:** fix wrong env path ([1270a68](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1270a68f35584c0854289064ef1e6bef89ee269a))
* **ci:** remove comment at yaml multi line ([e068a02](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e068a022de2a1b3a613452b189a4d7a14ed819f5))
* **ci:** remove redundant colon in docker run command ([c7e1f77](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/c7e1f778271b7d72070e0283dbb7b25c1fe4133e))
* **ci:** temp does not use secret of ci ([db58171](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/db581710f3e4bc63c6900c4a32d85d09c34702c3))
* **close:** fix len of Ticks error ([33aa605](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/33aa6051e0889e0d8b24ba0b12a9c05a7da49d78))
* **close:** fix try except then get zero close ([8b40bf0](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8b40bf0abcf813c6fb2e91396fc395542ba09d4c))
* **container:** add driver to docker network ([99ff4ae](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/99ff4aec783f42ac79de7282b112fe39485736b4))
* **container:** change env name to avoid docker host wrong ([80ed1db](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/80ed1db72221ab5af227a8361b6c72db56b02a10))
* **container:** fix missing encoding in bytes ([f29c8a3](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/f29c8a3d8f536fd80bce9c6ab4cdb6c17026f58a))
* **container:** fix the way use docker network ([0aa116f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/0aa116f6e1aa462f5ac6e158cc1bfe20cb0dc618))
* **grpc:** add queue full to avoid memory leak after client disconnect ([830c98e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/830c98e06b585969a417b2453163b785b6892aba))
* **grpc:** fix wrong augument in new server ([3b264d3](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/3b264d313cd3bdab9b88cea3e58d452dbec210f7))
* **heartbeat:** change the send heartbeat method to fix pika publish error ([71167c1](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/71167c131818468509730d97a9371a74edd3536e))
* **heartbeat:** fix debug has no initial ([9bbafae](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9bbafae4c88f45d731d2ffa6bc4b5f958f014192))
* **proto:** fix wrong compile proto script ([45210e2](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/45210e203c0daa3e8224002939c741d01e24d01c))
* **rabbitmq:** add process data to send heartbeat to avoid disconnect from rabbitmq ([1add815](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1add815f16c4b680a6bbf9fec2ce2edc755a7d64))
* **rabbitmq:** fix wrong delete exchange status code ([8b9884d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8b9884deb6fac959458f806352cf27ba6645b162))
* **shioaji:** add missing sleep in login fail ([f8cdd69](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/f8cdd69a8d01d1113312d90d3fedb9a6bcbde8f9))
* **simulation:** fix wrong logic in simulation buy ([a9d529b](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a9d529b3865691aae009ec82713c50e3fd602e90))
* **simulation:** key error when simulation trade in map of order count ([0248670](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/02486705c9b1ba90333018ba0a7f0fb42889b91e))

### Features

* **channel:** add all stream channel, sinopac trade method ([cb37927](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/cb379270f30a30667528bc1b2e10f2d233bb9070))
* **channel:** change data channel from rpc to rabbit mq ([68a9864](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/68a98648c5178c1b885f0ed3adec707b101e5d44))
* **close:** add check length of last count ([ccf122f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ccf122ff1a9d4ec8213a9afc0c30e4c961dd39cf))
* **close:** add sinopac api try get last count ([558926e](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/558926e329bbc24783527d7c300eb89a149e8086))
* **container:** add docker package to start rabbitmq container self ([8ef4288](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/8ef42888090858305387b99894450f2e880e6071))
* **container:** add except timeout error when terminate rabbitmq ([22ea974](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/22ea9749beabc3e24219eb7b45dd1689740ba879))
* **container:** add try except to request check health ([b9bffd2](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/b9bffd232d0cdac3018b6f85453c1919e1a637c3))
* **container:** change deployment network to host ([0dbfc0a](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/0dbfc0af93e36bef55ada6125586eed05f8d8077))
* **container:** change network mode to host ([fa415a1](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/fa415a11dee2f8345b2bbfd8df1ef3c1181cac0c))
* **container:** use rabbit api health check to check container is started ([4d8d313](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/4d8d3135cb38ac746df9b5ad8b0318fd12511f1f))
* **exception:** add try except in shioaji login to avoid login fail stuck ([296fc84](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/296fc8462cfa5f419338671cd20829965a3bf7e2))
* **grpc:** add stream callback, remove queue block ([ef6f839](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ef6f8391205c16802b153edb6743e268c62dc95b))
* **grpc:** add stream event to client, move sinopac callback to grpc, and set in workers ([654e64f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/654e64fa8421ebb29522fa7a9355327f5bbb1019))
* **grpc:** increase max message size to 1024*1024*1024 ([542d581](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/542d581263f5f2a1867fd8a3ac3b3ccf7b57689c))
* **health:** split grpc servicer, add debug mode for machine trading ([16e194d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/16e194dcb27e6fa490c3a63decedfb0937ac343f))
* **heartbeat:** add heartbeat to detect client healthy, remove server token ([ca97035](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/ca97035089407106bbbaa912d15690739275cf4e))
* **history:** add history kbar, close ([2b16bdd](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/2b16bdd2b43f47702a6d4557946d784ba5a193e7))
* **history:** add History Tick rpc ([60acb68](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/60acb6858f7920446689b483622772b68ec292bc))
* **layout:** add grpc and sinpac class alpha ([87093d8](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/87093d8e2b3be1cdbdd969292775d7e05139a9d5))
* **layout:** let all file in same module, add load .env ([389582f](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/389582fb14974fe44ab53283fadbf3969d3990ad))
* **login:** extend system maintenance wait time to 75 sec ([5d46f6d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5d46f6d23d5312b662c393a504b6aa53000931b7))
* **login:** remove check need fetch, update shioaji to 0.3.6.dev1 ([3b3dd4d](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/3b3dd4d1963191537d35b69df1d71dfb25e60004))
* **performance:** add sinopac worker class to get best connection ([9f85f48](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9f85f488d0d1f1ebf028e7a050a7551e337b9cf7))
* **python:** upgrade to 3.10, fix new pylint warning ([31607fb](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/31607fb0dbe8ef8f895836a655e056fd194f9ebb))
* **rabbitmq:** deprecate run rabbitmq conatiner, put it into ci, only reset exchange in startup ([73226b3](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/73226b30f073d276f6041a7f4af0d77acc11a33c))
* **secret:** add rabbit container secret to env file ([52312b4](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/52312b48ab001098b9b993daf0d002e66947f089))
* **shioaji:** revert to 0.3.5.dev1 ([5184c34](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5184c3408352268fd9c8e4b03db0bdcc9cbf4cd7))
* **shioaji:** update ver to 0.3.6.dev0 ([9fd86ac](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/9fd86ac30f9f7660b1f65e3033798696d9f8dbf6))
* **sinopac:** add constant, add main worker, add fill local stock list, order status ([1b4f528](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/1b4f5287a7325785f6a346aa064a65e4934a06e2))
* **sinopac:** finish multi login ([351b095](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/351b09511ea028d15275326526d613b39c2a8fba))
* **snapshot:** add snapshot by stock, multi threading of connection alpha ([608b5cd](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/608b5cd5d174200ec9d63d6b3ae59f01012d8bc1))
* **stock:** add rpc GetAllStockDetail method ([4ad1d94](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/4ad1d94e31f52e8f0bfbfbe99f94ccd660d59639))
* **subscribe:** add subscribe unscribe tick, bidask, add volume rank ([e763778](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/e76377843d4fba7e10bc57672f506fad9f4fd911))
* **subscribe:** add unsubscribe all, add last sucess fetch file ([a46bf97](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/a46bf97b97affd9fddfc57a5ac0c70d88a933de1))
* **thread:** change get history tick to multi threads ([bf09445](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/bf09445d62c05b5206348cfeb36b4a76967f8ff5))
* **timeout:** add timeout check in ticks, kbar ([987ce14](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/987ce14d7e7c690af90d69045a54d4253a3d0b98))
* **trade:** add trade service, schedule exit, env class, move project layout ([5ef42ad](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/5ef42adfd008c37bd47df9a70da6fea7b93229ff))
* **tse:** change GetStockSnapshotTSE return single message ([f9ed67b](https://github.com/ToC-Taiwan/toc-sinopac-python/commit/f9ed67b53b2845cf3358408b893291eee80974ea))
