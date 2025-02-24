# nginx-conf-tool

This package introduces a command `nct` with sub-commands.

# Installation

    pip install nginx-conf-tool

# The Tree Subcommand

This sub command will scan the nginx.conf file and display its structure as a tree:

    $ nct tree <path-to-nginx.conf>
    $ nct tree /etc/nginx/nginx.conf