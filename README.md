# Twitter scripts

## Nuke my tweets

Deletes all tweets from a twitter account using twitter history. Has the option to preserve tweets.

## Follow my minions

Add all twitter accounts in a csv file as friend on twitter.

## How does it work?

It uses the twitter archive and twitter api to find tweets by id and delete them one by one.

### Set up

-   [1] Make a new app at https://apps.twitter.com/
-   [2] Create an Access token for it
-   [3] Download this git repository
-   [4] Install and activate the virtual environment
-   [5] Rename file `scripts_template.ini` to `scripts.ini`
-   [7] Fill the details in `scripts.ini` file
-   [8] Execute command `python3 file_name.py` for a dry run
-   [8] Execute command `python3 file_name.py -a` to wreck yourself

## License

Nuke Tweets is released under MIT license
