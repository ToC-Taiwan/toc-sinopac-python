# (2022-06-08)

## CHANGELOG

### Bug Fixes

* **grpc:** add queue full to avoid memory leak after client disconnect ([830c98e](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/830c98e06b585969a417b2453163b785b6892aba))
* **proto:** fix wrong compile proto script ([45210e2](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/45210e203c0daa3e8224002939c741d01e24d01c))

### Features

* **channel:** add all stream channel, sinopac trade method ([cb37927](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/cb379270f30a30667528bc1b2e10f2d233bb9070))
* **grpc:** add stream event to client, move sinopac callback to grpc, and set in workers ([654e64f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/654e64fa8421ebb29522fa7a9355327f5bbb1019))
* **history:** add history kbar, close ([2b16bdd](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/2b16bdd2b43f47702a6d4557946d784ba5a193e7))
* **history:** add History Tick rpc ([60acb68](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/60acb6858f7920446689b483622772b68ec292bc))
* **layout:** add grpc and sinpac class alpha ([87093d8](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/87093d8e2b3be1cdbdd969292775d7e05139a9d5))
* **layout:** let all file in same module, add load .env ([389582f](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/389582fb14974fe44ab53283fadbf3969d3990ad))
* **performance:** add sinopac worker class to get best connection ([9f85f48](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/9f85f488d0d1f1ebf028e7a050a7551e337b9cf7))
* **python:** upgrade to 3.10, fix new pylint warning ([31607fb](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/31607fb0dbe8ef8f895836a655e056fd194f9ebb))
* **sinopac:** add constant, add main worker, add fill local stock list, order status ([1b4f528](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/1b4f5287a7325785f6a346aa064a65e4934a06e2))
* **sinopac:** finish multi login ([351b095](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/351b09511ea028d15275326526d613b39c2a8fba))
* **snapshot:** add snapshot by stock, multi threading of connection alpha ([608b5cd](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/608b5cd5d174200ec9d63d6b3ae59f01012d8bc1))
* **stock:** add rpc GetAllStockDetail method ([4ad1d94](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/4ad1d94e31f52e8f0bfbfbe99f94ccd660d59639))
* **subscribe:** add subscribe unscribe tick, bidask, add volume rank ([e763778](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/e76377843d4fba7e10bc57672f506fad9f4fd911))
* **thread:** change get history tick to multi threads ([bf09445](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/bf09445d62c05b5206348cfeb36b4a76967f8ff5))
* **trade:** add trade service, schedule exit, env class, move project layout ([5ef42ad](https://gitlab.tocraw.com/root/toc-sinopac-python/commit/5ef42adfd008c37bd47df9a70da6fea7b93229ff))
