# Flask Micro Service: Logging

This is my first attempt at creating a RESTful micro service.  It's purpose to to allow log aggregation from multiple 
services to be centrally stored on a single service.
 
I haven't flushed this out completely, I keep trying new things with Flask so some projects only get 80% of the way
done before I'm chasing the next rabbit, but this one at least works.

Requirements:
```
Flask
Flask-SQLAlchemy
```

Like my other projects, this has a build script and a run script.

Using the `build.py` script will populate the database.  Note that if you're using MySQL or RDS service like that
you may need to run `CREATE DATABASE name_your_database` as the build script does not currently handle creating the
database itself, just the tables based off the model.  If you're using SQLite, you should be able to just rock and
roll.

Before running `build.py` or `run.py` be sure to check out the Config object and update the settings as you need.
Within the `fmslogging.config.Config` object you can setup defaults if you'd like, otherwise, you can simply over
write the configuration settings in the `build.py` or `run.py`.

When you execute `run.py` it will launch the Flask service.

This will setup a default **privileged** service call test_service.  This is just for the sake of testing and should
not be used for anything for real, not that this is really a production ready service.

To create a log record you'll need to build a JSON object and send it to the `/intake` end point.  The structure of
the request is as follows:
```
{
    "key": "service-key-as-a-string",
    "data": [
        {
            "level": "string-level",
            "timestamp": "YYYY-MM-DD HH:MM:SS",  /* ISO 8601 formatted date stamp */
            "body": "body-of-message"
        },
        {
            "level": "string-level",
            "timestamp": "YYYY-MM-DD HH:MM:SS",  /* ISO 8601 formatted date stamp */
            "body": "another-body-of-message"
        },
    ]
}
```

As you can see by the example, you can send multiple messages at a time.  Note that the date is format sensitive and
should be formatted as YYYY-mm-DD HH:MM:SS.

Level can be anything you'd like, but the defaults are:
```
debug
info
warning
error
critical
```

Any other strings passed for the level will show up as `not_set` on the record.

Right now, there are no restrictions are the querying element and it's not super sophisticated due to some issues
with the way SQLAlchemy handles it's query filtering.  You can query based off the service name, log levels and 
dates.  You can also apply a date to the service and level requests.

These requests should be sent to the `/query` end point and will take the following formats:

```
/query/service/<service-name>
/query/service/<service-name>/<date>
/query/service/<log-level>
/query/service/<log-level>/<date>
/query/service/<date>
```

I plan to work on this and make it a bit more robust at some point, but I have to work out the SQLAlchemy issues first.

I'm also planning to add (and have frame-worked out) a method for purging records (deleting them) as well as a way to
add new services.