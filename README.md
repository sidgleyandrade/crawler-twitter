# crawler-twitter

crawler-twitter is an implementation multi-bounding-box using tweepy and postgresql to collect and store tweets (structured and json format).

## Dependencies

* python 2.7 or greater
* libraries available in the `requirements.txt` file
* PostgreSQL 9.5 or greater
* PostGIS 2.0 or greater

## Configuration

* To create a database with the extension postgis. It is not necessary to create tables, crawler-twitter will create the tables from the config file parameters (`segup.cfg`).
* To configure the connections in the `setup.cfg` file, as follow:

    * __Bounding box connection__

    ```
    [connection_name]
    connection.user=nickname
    connection.consumer_key=abc66UABCabcabc000abc0ABab
    connection.consumer_secret=abc66UABCabcabc000abc0ABab
    connection.access_token=123-abc66UABCabcabc000abc0ABab
    connection.access_token_secret=123-abc66UABCabcabc000abc0ABab
    connection.bounding_box=-74.0,-33.9,-28.6,5.3
    connection.search_word=
    database.host=MyHost
    database.schema=MyShcema
    database.name=MyDatabase
    database.table=MyTableName
    database.user=MyUserName
    database.password=MyPassword
    ```
        
    * __Search word connection__

    ```
    [connection_name]
    connection.user=nickname
    connection.consumer_key=abc66UABCabcabc000abc0ABab
    connection.consumer_secret=abc66UABCabcabc000abc0ABab
    connection.access_token=123-abc66UABCabcabc000abc0ABab
    connection.access_token_secret=123-abc66UABCabcabc000abc0ABab
    connection.bounding_box=
    connection.search_word=rainfall
    database.host=MyHost
    database.schema=MyShcema
    database.name=MyDatabase
    database.table=MyTableName
    database.user=MyUserName
    database.password=MyPassword
    ```

**Note:** `connection.bounding_box` and `connection.search_word` are exclusive parameters.


## Running

    $ ./run.sh

## Contact

If you believe you have found a bug, or would like to ask for a feature or contribute to the project, please inform me at sidgleyandrade@utfpr.edu.br.

## License

This software is licensed under the GPLv3.
