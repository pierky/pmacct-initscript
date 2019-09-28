# pmacct Systemd initscripts

Systemd scripts for **pmacct** suitable for RedHat and Debian Linux flavours

## Introduction
The scripts in the `system` directory can be used to manage the various **pmacct** `systemd` daemons with the usual commands such as:

```
systemctl enable daemon.service
systemctl disable daemon.service
systemctl start daemon.service
systemctl stop daemon.service
```

## Assumptions
The original scripts were extracted from a `pmacct` RPM with minor modifications to make them work with a **default** installation of `pmacct`.  

If you have modified the location of the `pmacct` executables during installation, then you will have to edit each file in the `system` directory to reflect this change. The scripts assume the executables can be found in the `/usr/local/sbin/pmacctd` directory

## Installation
Run the `systemd/bin/install_systemd.py` script. There should be sufficient error messages to assist you in fixing any simple issues. 

The output of a successful run should look like this:

```
$ sudo systemd/bin/install_systemd.py 
SUCCESS! You are now able to start/stop and enable/disable the following systemd services: pmbmpd.service, nfacctd.service, pmacctd.service, pmbgpd.service, pmtelemetryd.service
$
```

## Configuration

The installation `systemd/bin/install_systemd.py` script will make the following services available to `systemd`

```
nfacctd.service
pmacctd.service
pmbgpd.service
pmbmpd.service
pmtelemetryd.service
sfacctd.service
```

Each service will look for its respective configuration file in the `/etc/pmacct` directory. Make sure the daemon name you are working with has an equivalent configuration filename.

1. nfacctd.service will need a `/etc/pmacct/nfacctd.conf` file.
1. pmacctd.service will need a `/etc/pmacct/pmacctd.conf` file.
1. pmbgpd.service will need a `/etc/pmacct/pmbgpd.conf` file.
1. pmbmpd.service will need a `/etc/pmacct/pmbmpd.conf` file.
1. pmtelemetryd.service will need a `/etc/pmacct/pmtelemetryd.conf` file.
1. sfacctd.service will need a `/etc/pmacct/sfacctd.conf` file.

Details of what each configuration file should contain is in the `pmacct` documentation.

**NOTE:** 

There are some things to note.

1. The service scripts **do not** support multiple daemon instances. You will have to make custom modifications to support this.
1. The service scripts **do not** support the use of an `EnvironmentFile` in the `/etc/systemd` directory or anywhere else. Put all your configuration directives in the `/etc/pmacct` directory.

