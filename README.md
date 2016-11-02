# crawler-twitter
crawler-twitter -- is a implementation using the tweepy module  to collect and store tweets in postgresql

## Dependencies

* python 2.7
* modules available in the file requirements.txt
* postgresql
* postgis

### Installation

* To create a database with the extension postgis. It is not necessary to create tables, the crawler-twitter create the tables from template (template-table.sql)
* To configure the file setup.cfg

## Environment configuration

### Virtualenv

    $ chmod +x crawler-twitter-cfg-env.sh
    $ ./crawler-twitter-cfg-env.sh

### no Virtualenv
* To install all python modules  (requirements.txt)

## Usage

     $ source .virtual/bin/activate
     $ python crawler-twitter.py
     
## Contact

If you believe you have found a bug, or would like to ask for a feature, please inform me at sidgleyandrade@utfpr.edu.br.

## License

This software is licensed under the GPLv3.
