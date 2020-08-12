# Shortener Explorer

A simple utility for exploring URL shorteners safely.

Step 1 - git clone
`git clone https://github.com/5hu5ky/shortener_explorer`

Step 2 - install dependencies

```
pip3 install -r requirements.txt
python3 url_explorer.py --help
```



Optional Step - If you want to run this in a virtual environment (in this example your environment name is venv; change it if you need to):

```
pip3 install virtualenv
python3 -m virtualenv <url_capture_path>/venv
cd <url_capture_path>
source ./venv/bin/activate
./venv/bin/pip3 install -r ./requirements.txt
python3 url_explorer.py --help
```

# Help Documentation

```
usage: url_explorer.py [-h] [-s SERVICE | -u URL] [-l LIMIT]
                       [--hashlength HASHLENGTH] [-c CAMPAIGN]
                       [--clickthrough] [-e] [-p EVIDENCEPATH]
                       [--search SEARCH] [-w] [-v] [-d]

Scan link shortener services... Version 1.1

optional arguments:
  -h, --help            show this help message and exit
  -s SERVICE, --service SERVICE
                        Service URL - e.g. https://bit.ly
  -u URL, --url URL     Single URL to check
  -l LIMIT, --limit LIMIT
                        Loop limit - 0 will loop through all permutations
  --hashlength HASHLENGTH
                        Adjust hashlength - default is 6 characters
  -c CAMPAIGN, --campaign CAMPAIGN
                        Campaign name - establishing a campaign name you can
                        create continuity for tags scanned...
  --clickthrough        Click through spam warning displayed - only works for
                        bit.ly for now...
  -e, --evidence        Enable screen captures
  -p EVIDENCEPATH, --evidencepath EVIDENCEPATH
                        Evidence storage path
  --search SEARCH       One or list of search strings - lists should be comma
                        separated strings. If a search string is defined
                        captures will happen only if there is a match...
                        Search is case insensitive.
  -w, --writelog        Enable logging - logs are written to the application
                        directory; if there is a campaign defined it will be
                        written to the campaign directory.
  -v, --verbose         Enable verbose mode
  -d, --debug           Debug mode

```

## Capabilities
1. Explore Single URL - this can be any URL 
2. Explore Service - service in this context is a link shortener service, when you choose this option you need to define a `limit` and ideally your target `hashlength`; the default hashlegnth is 6. 
3. Conditional captures based on a single string or a list of search strings - helps filter out junk...
4. Search campaigns - this lets you retain a history of hashes tested so that they will not be included next time you run the same campaign. Campaigns keep different log files for different missions. Number of log files in a campaign folder is the number of missions run. Each log file contains entries for successful captures.
5. `clickthrough` - [Only for bit.ly pages] - if the site in question is marked as a spam site, bit.ly will display a message indicating this finding interrupting the scan, setting this option allows you to skip past this interruption.


#Usage Examples

###Single URL screen capture - this can be a URL for shortener service or a regular URL

**Example regular URL:**

```
python3 url_explorer.py -u https://www.somesite.com

```

**Example shortener URL:**

```
python3 url_explorer.py -u https://bit.ly/bbyH6O 
```


### Batch scan URL shorteners - you can define a service provider and the length of hashes you want to capture

**Randomly explore 5 URLs from bit.ly (default hash length is 6)**

```
python3 url_explorer.py -s https://bit.ly -l 5 --hashlength 6
```

**Randomly explore 10 URLs from bit.ly with hash length 8**

```
python3 url_explorer.py -s https://bit.ly -l 10 --hashlength 8
```

### Evidence Collection
**Creates screen captures of explored pages**

```
python3 url_explorer.py -s https://bit.ly -l 10 --hashlength 8 -e -p /home/user/evidence
```

If the path does not exist the script will ask you if it should create it...


### Campaign Use

**Example of campaign use with search words:**
Campaign is just a string, a folder with that string will be created under the `--evidencepath` if there is no evidence path is defined evidence path becomes `./evidence` - making your campaign folder `./evidence/<campaign_name>`
    
```
python3 url_explorer.py -s https://bit.ly/ -e -p ./evidence_folder -w -v --clickthrough -l 5 --search twitter,"san francisco",facebook --campaign test_campaign
```


# Maintenance Related
    
#TODO:
    1. Detect keyboard Ctrl+C for long loop cycles
    2. User-Agent randomization
    3. Word Freq analysis on web pages
    4. Create an option that tries combinations instead of permutations...
    5. Create an argument for consuming hashes via file - targeted hash checks...
    6. Analytic improvements
    
#DONE:
    1. Auto platform geckodrive detection - DONE
    2. Implement a limit in case you do not want to run this infinitely. - DONE
    3. Implement command line args - DONE
    4. PhantomJS does not work on Windows - REMOVE - DONE
    5. Implement a Queue so that there is a limit to threads - DONE
    6. Create an output folder for the mission and logs - DONE
    7. Write the hashes to a file before exiting... - DONE [only in campaign mode]
    8. Check if there is a list of checked hashes exists  hash:service if yes, load them up in to `__CHECKED_HASH` - DONE [only in campaign mode]
    -- Keep the hashes per mission if the evidence path has the hash list, use it...
    9. Filters - for notifications for areas of interest (keywords) - DONE
