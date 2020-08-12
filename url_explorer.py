'''
Created on Aug 12, 2020

@author: main_man
'''
import argparse
import sys
import os
from collections import Counter
import json

from uxp.http_url.explorer import Explorer
from uxp.common.tools import Tools

if __name__ == '__main__':
 
    parser =argparse.ArgumentParser(description="Scan link shortener services... Version 1.1")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--service', help='Service URL - e.g. https://bit.ly')
    group.add_argument('-u', '--url', help='Single URL to check')
    
    parser.add_argument('-l', '--limit', help='Loop limit - 0 will loop through all permutations', required=False)
    parser.add_argument('--hashlength', help='Adjust hashlength - default is 6 characters')
    parser.add_argument('-c', '--campaign', help='Campaign name - establishing a campaign name you can create continuity for tags scanned...')
    parser.add_argument('--clickthrough', help='Click through spam warning displayed - only works for bit.ly for now...', action='store_true')
    parser.add_argument('-e', '--evidence', help='Enable screen captures',action='store_true')
    parser.add_argument('-p', '--evidencepath',help='Evidence storage path')
    parser.add_argument('--search',help='One or list of search strings - lists should be comma separated strings. If a search string is defined captures will happen only if there is a match... Search is case insensitive.')
    parser.add_argument('-w', '--writelog', help='Enable logging - logs are written to the application directory; if there is a campaign defined it will be written to the campaign directory.',action='store_true')
    parser.add_argument('-v', '--verbose', help='Enable verbose mode',action='store_true')
    parser.add_argument('-d', '--debug', help='Debug mode',action='store_true')
    
    args = parser.parse_args()
    
    #DEFAULT VALUES
    service = Explorer.service
    limit = 0 #limit 0 runs infinitely
    hashlength = 6
    debug = False
    writelog = False
    verbose = False
    screencap = False
    clickthrough = False
    evidencepath="./evidence"
    search = []
    
    if not args.service and not args.url:
        print("A target service or a URL must be defined!")
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    if args.service and not args.limit:
        print("Define a limit for your scan - `0` will test all permutations.")
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    if args.url and args.limit:
        print("You are scanning a single URL a limit cannot be defined!")
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    if args.limit is not None:
        try:
            limit = int(args.limit)-1
        except:
            print("Limit needs to be an integer!")
            parser.print_help(sys.stderr)
            sys.exit(1)
    
    if args.service is not None:
        service = args.service
        
    if args.hashlength is not None:
        hashlength = args.hashlength
        
    if args.debug is not None:
        debug = args.debug
        
    if args.verbose:
        verbose = True

    if args.debug is not None:
        debug = True
            
    if args.evidence:
        screencap = True
        
    if args.clickthrough:
        clickthrough = True
    
    if args.search:
        if args.search.find(",") != -1:
            search = [x.strip() for x in args.search.split(',')]
        else:
            search.append(args.search)
    
    if args.evidencepath and not args.campaign:
        res = Tools.directoryManager(args.evidencepath)
        if  res == None:
            os.makedirs(evidencepath)
        else: 
            evidencepath = res
    elif args.evidencepath and args.campaign:
        res = Tools.directoryManager(args.evidencepath,args.campaign)
        if res == None:
            os.makedirs(evidencepath)
        else: 
            evidencepath = res
    else:
        evidencepath = Tools.directoryManager(evidencepath,ask=False)
        

    try:
        result = []
        if args.url:
            bitlyExplorer = Explorer(evidenceCollect=screencap, evidenceSavePath=evidencepath, search=search, debug=debug, verbose=verbose, log=args.writelog)
            if args.campaign:
                bitlyExplorer.setCampaign(args.campaign)
            bitlyExplorer.setClickThrough(clickthrough)
            result.append(bitlyExplorer.linkFetcherWorker(urlhashx=args.url))
        else:
            bitlyExplorer = Explorer(shortnerService=service, hashLength=hashlength, evidenceCollect=screencap, evidenceSavePath=evidencepath, search=search, debug=debug, verbose=verbose, log=args.writelog)
            if args.campaign:
                bitlyExplorer.setCampaign(args.campaign)
            bitlyExplorer.setClickThrough(clickthrough)
            result = bitlyExplorer.linkFetcher(count=limit)
            
        print("HTTP Response Summary:")
        print(json.dumps(Counter(result),indent=4))

    except Exception as ex:
        print(ex)
        parser.print_help(sys.stderr)
        sys.exit(1)
    