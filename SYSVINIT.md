# pmacct System V initscript

This script is aimed to manage multiple instances of pmacct daemons
(http://www.pmacct.net/ by Paolo Lucente)

For each daemon (pmacctd|nfacctd|sfacctd|uacctd), one or more
instances may be managed; instances are mapped one-to-one to
configuration files that are in the $CONFIG_DIR directory
(/etc/pmacct by default). Configuration files' names must
follow this schema:

 *daemon_name*[.*instance_id*].conf

An instance's name is composed by the name of the daemon + "." +
an optional instance ID; if the instance ID is omitted the
"default" ID is used.

 Example:

 ```
 pmacctd.conf ---> daemon = pmacctd, instance = "pmacctd.default"

 pmacctd.2.conf -> daemon = pmacctd, instance = "pmacctd.2"

 nfacctd.1.conf -> daemon = nfacctd, instance = "nfacctd.1"
 ```

The second argument of this script may be used to selectively start/stop a single instance; if omitted, all the instances are started/stopped:

 Example:

 ```
 /etc/init.d/pmacct start pmacctd.default

 service pmacct stop nfacctd.1
 ```

Daemons are started with -D option (Daemonize) and with
-F option (PID file) pointing to $PIDDIR/<instance_id>
(PIDDIR default to /var/run/pmacct). It's safe to avoid
using the "pidfile" and "daemonize" keys in the configuration
file.
