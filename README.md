Psst is a simple password generator for test deployments.

#Usage

Psst can generate multiple passwords for different use cases and returns them in a JSON formatted string.

A configuration file for Psst looks like this

        psst:
            services: 
                - "db_root"
                - "user1"
                - "user2"
            length: 20

Inside the `psst` field is the configuration for Psst.
The service field is a list of names for which a password is needed.
In this example we need a password for the database root and a password for two users.

The following command executes Psst

    psst <configuration file>

Psst reads in the configuration file an creates a random password for every name in service.
The length in the configuration file defines the length of the passwords.

By running with the example configuration file we get

    $psst conf.json
    {
      "db_root": "KQHsICLCP3vHZOK3jxnd",
      "user1": "znHPUJmeAd2XLz48h8J3",
      "user2": "5zcMhJfhOq6ZampiPOXR"
    }


The output of Psst can be used in shell scripts with the help of `jq`.

    eval $(psst conf.json | jq -r '@sh "alice=\(.user1) bob=\(.user2)"')

#Configuration

Psst has the following options in its configuration file

1. passwords a list of names for the passwords to be generated
2. length a positive number that is the lenght of generated the passwords (default: 20)
3. choices a string with characters that are used to create the password (default: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@`)
