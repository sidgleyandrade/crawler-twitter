# crawler-twitter

**crawler-twitter** is an implementation multi-bounding-box using tweepy and postgresql to collect and store tweets (structured and json format).

## Dependencies

* python 2.7 or greater
* python-virtualenv 15.1 or greater
* libraries available in the `requirements.txt` file
* PostgreSQL 9.5 or greater
* PostGIS 2.0 or greater

## Instalation

    $ git clone https://github.com/sidgleyandrade/crawler-twitter.git    
    
## Configuration

* To create a database with the extension postgis. It is not necessary to create tables, **crawler-twitter** will create the tables from the config file parameters (`segup.cfg`).
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

#### Getting Twitter credentials for apps
 
See [https://apps.twitter.com/](https://apps.twitter.com/).

## Running

    $ chmod +x run.sh
    $ ./run.sh

## Demo Video

[![Crawler-Twitter tool](https://i9.ytimg.com/vi/i2dgaFrxiHs/mqdefault.jpg?sqp=CIjUod4F&rs=AOn4CLDkxFH3sZ6TKmivRAbDNJHtAmf1ww&time=1539861235385)](http://www.youtube.com/watch?v=i2dgaFrxiHs "Crawler-Twittre tool")

## Citation

Please, cite the conference poster if you use this tool in your research:

    Sidgley Camargo de Andrade, Lieverton Horn Queiroz, Alexandre C. B. Delbem, João Porto de Albuquerque (2018)
    'An architectural model for retrieving data from Social Media APIs: an instantiation for consuming the Twitter Stream API'.
    Presented as poster. In: XIX Brazilian Symposium on Geoinformatics (GEOINFO). Campina Grande, Paraíba, Brazil.

BibTex

    @misc{deAndrade2018c,
        author = {{Sidgley Camargo de Andrade} and {Lieverton Horn Queiroz} and {Alexandre C. B. Delbem} and {Jo\~{a}o Porto de Albuquerque}},    
        title = {{An architectural model for retrieving data from Social Media APIs: an instantiation for consuming the Twitter Stream API}},
        month = {12},
        year = {2018},
        type = {Poster},
        howpublished = {Presented as poster},
        note = {In: XIX Brazilian Symposium on Geoinformatics (GEOINFO). Campina Grande, Para\'{i}ba, Brazil},
        url = {https://www.researchgate.net/publication/330221368_An_architectural_model_for_retrieving_data_from_Social_Media_APIs_an_instantiation_for_consuming_the_Twitter_Stream_API/stats}
    }

## Known issues

See [issues](https://github.com/sidgleyandrade/crawler-twitter/issues).

## Contact

If you believe you have found a bug, or would like to ask for a feature or contribute to the project, please inform me at sidgleyandrade[at]utfpr[dot]edu[dot]br.

## License

This software is licensed under the GPLv3.
