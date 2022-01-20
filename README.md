# Smart Plug Control Platform
![CI](https://github.com/Eryalito/smap-cp/actions/workflows/ci.yml/badge.svg)
![Lastest build](https://github.com/Eryalito/smap-cp/actions/workflows/container_latest.yml/badge.svg)

Smart Plug Control Platform (SMAP-CP) is an application designed to manage electrical devices automatically through smart plugs.
## Description
Configuration parameters are defined inside a config file in yaml format. Devices, cache configuration, database configuration and application configuration is loaded from this [file](config.yaml).
```yaml
devices:
  - name: Human readable device name
    id: xxxxxxxxxxxxxxxxxxx
    key: yyyyyyyyyyyyyyyyy
    ip: '192.168.2.82'
    version: '3.3'
    steps:
      - days: 0-6 # wwek days 0 - Monday : 6 - Sunday
        start: 00 # start at 00:00
        end: 24 # end at 24:00
        count: 3 # switched on for 3 hours in the period
        timezone: CET

cache-config:
  type: redis
  prefix: smap-cp- # key prefix
  host: localhost

database-config:
  type: sqlite
  file: database.db
  prefix: '' # table prefix

application-config:
  timer: 10
  timezone: UTC
```
Let's dig in into the fields:
- **devices**: it's an array of devices, containing all the information about the smart plugs.
  - **name**: It's a human name to easily locate the devices in large config files.
  - **id**: Device id used for contacting it
  - **key**: Pre-shared key for encrypting device communications
  - **ip**: Device IP
  - **version**: Installed software version
  - **steps**: List of time intervals
    - **days**: weekdays to apply the interval
    - **start**: start hour of interval (24 hours)
    - **end**: end hour of interval (24 hours)
    - **count**: number of hours active for the interval
    - **timezone**: should match Ree timezone (CET)
- **cache-config**: cache configuration
  - **type**: cache type *(currently only redis)*
  - **prefix**: cache key prefix
  - **host**: cache server IP
- **database-config**: database configuration
  - **type**: database type *(currently only sqlite)*
  - **file**: database file
  - **prefix**: table prefix
- **application-config**: application config
  - **timer**: time in seconds between executions
  - **timezone**: Application timezone. Should not be changed

## How it works
The application first loads and verifies all of the configuration from the config.yaml. *(This means that the file is just read and needed on the application initialization)*. The device information is loaded into cache, so it can be edited between each iteration. The orchestrator will periodically load device information and check if the device should be turned on in the moment. If so, it'll turn it on for a predefined period of time (currently 3 times the time beetween executions). The orchestrator will find the cheaper hours in the interval according to the [Ree](https://www.ree.es/es).

## How to run it
### As application
Just run the `main.py` file from the root folder.
### As a container
The application can be executed as a container. There are a lot of ways of running it, but the common one is to mount a volume in the container with the configuration file.
```bash
docker run -v ./config.yaml:/repo/config.yaml --workdir=/repo eryalus/smap-cp:latest
```