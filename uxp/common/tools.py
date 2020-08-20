'''
Created on Jul 25, 2020

@author: main_man
'''

import sys
import os
from subprocess import Popen
import subprocess


class Tools(object):
    '''
    Miscellaneous support functions 
    '''
    @staticmethod
    def get_platform():
        platforms = {
            'linux1' : 'Linux',
            'linux2' : 'Linux',
            'darwin' : 'OS X',
            'win32' : 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        
        return platforms[sys.platform]  
    
    @staticmethod
    def run_external(args):
        proc = Popen(args, stdout=subprocess.PIPE)
        outx, _ = proc.communicate()
        proc.wait()
        result = list(filter(None,outx.decode('utf-8').split('\n')))

        return proc.returncode, result
    
    @staticmethod
    def which(program):
        def is_exe(fpath):
            try:
                return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
            except:
                pass
        '''
        fpath = None
        fname = None
        try:
            fpath, fname = os.path.split(program)
        except:
            pass
        
        if fpath in locals():
        '''
        if is_exe(program):
            return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None
    
    @staticmethod
    def permutation(n,hash_size):
        '''
        Simple permutation function
        '''
        fact = 1
        for i in range(n-hash_size+1,n+1): 
            fact = fact * i 
            
        return fact
    
    @staticmethod
    def query_yes_no(query, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid answer: '%s'" % default)
        try:
            while True:
                    sys.stdout.write(query + prompt)
                    choice = input().lower()
                    if default is not None and choice == '':
                        return valid[default]
                    elif choice in valid:
                        return valid[choice]
                    else:
                        sys.stdout.write("Please respond with 'yes' or 'no' "
                                         "(or 'y' or 'n').\n")
        except:
            print("Program abruptly exited!")
            sys.exit(1)
    
    @staticmethod
    def directoryManager(basepath,missionpath=None, ask=True):
        if missionpath:
            basepath = os.path.join(basepath,missionpath)
        if not os.path.exists(basepath):
            if ask:
                response = Tools.query_yes_no("{} does not exist - create it?".format(basepath))
            else:
                response = True
            if response:
                os.makedirs(basepath)
                #evidencepath = basepath
            else:
                return False #print ("Writing to ".format(evidencepath))
            
            #os.makedirs(basepath)
        return basepath 
    
    



    @staticmethod
    def resultWrite(filepath, content):
        try:    
            with open(filepath,"a+") as filex:
                filex.write(content +"\n")
        except: 
            return False
        return True
    
    
    @staticmethod
    def readHashList(filepath):
        result = set()
        try:    
            with open(filepath,"r") as filex:
                for line in filex:
                    result.add(line.strip("\n"))
        except: 
            pass
        return result
    
if __name__ == '__main__':
    print(Tools.getFile("http_url://huskersgameday.com/2010/11/09/texas-am-announces-that-12th-man-day-will-be-november-20th-against-nebraska/", "aFw2Aj"))