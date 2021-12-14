# Smart Plug Control Platform
Smart Plug Control Platform (SMAP-CP) is an application designed to manage electrical devices automatically through smart plugs.
## Description
----
Configuration parameters are defined inside a config file in yaml format. Devices, cache configuration, database configuration and application configuration is loaded from this file.
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
        count: 24 # switched on for 3 hours in the period

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

## How it works
----
The application first loads and verifies all of the configuration from the config.yaml. *(This means that the file is just read and needed on the application initialization)*. The device information is loaded into cache, so it can be edited between each iteration. The orchestrator will periodically load device information and check if the device should be turned on in the moment. If so, it'll turn it on for a predefined period of time (currently 3 times the time beetween executions). The orchestrator will find the cheaper hours in the interval according to the [Ree](https://www.ree.es/es).
