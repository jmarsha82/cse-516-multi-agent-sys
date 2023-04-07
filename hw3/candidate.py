#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re #regular expression

inputFile = 'ED-00016-00000001.txt'

plural = []
borda = []
approval = []

runoff = []
eliminated = []

#matching rules
valid_regex = re.compile(r"[[0-9,. \t]+$")
number_regex = re.compile(r"\d+")
numberEnd_regex = re.compile(r"\d+$")

def count(): 
    try:
        file = open(inputFile, 'r')
        for line in file:
            if len(plural) == 0:
                number = numberEnd_regex.match(line)
                if number is not None:
                    for i in range(0, int(line)):
                        plural.append(0)
                        borda.append(0)
                        approval.append(0)
                    continue
            
            valid = valid_regex.match(line)
            if valid is not None:
                matches = number_regex.findall(line)
                
                #validate preference range
                isValid = True
                for i in range(1, len(matches)):
                    can = int(matches[i])
                    if can > len(borda):
                        isValid = False
                if isValid:
                    time = int(matches[0])
                    
                    #plural
                    can = int(matches[1])
                    plural[can-1] += time
    
                    #borda
                    for i in range(1, len(matches)):
                        can = int(matches[i])
                        borda[can-1] += (len(borda)-i)*time
                        
                    #approval
                    for i in range(1, len(matches)):
                        can = int(matches[i])
                        approval[can-1] += time
        print("Plurality vote: %s " % plural)
        print("Borda count: %s " % borda)
        print("Approval vote: %s " % approval)
    except IOError:
        sys.exit("IOE Error: Fail to open %s !" % inputFile)
    else:
        file.close()

def eliminate(): 

    try:
        numOfCan = len(runoff)
        for i in range(numOfCan):
            runoff[i] = 0
        
        file = open(inputFile, 'r')
        for line in file:
            valid = valid_regex.match(line)
            if valid is not None:
                matches = number_regex.findall(line)
                
                #validate preference range
                isValid = True
                for i in range(1, len(matches)):
                    can = int(matches[i])
                    if can > len(borda):
                        isValid = False
                if isValid:
                    time = int(matches[0])
                    hasCount = False
                    #runoff
                    #score = numOfCan
                    for i in range(1, len(matches)):
                        can = int(matches[i])
                        if not eliminated[can-1] and not hasCount:
                            #score -= 1
                            #runoff[can-1] += score*time
                            runoff[can-1] += time
                            hasCount = True
                            
        index = 0
        minValue = 99999
        for i in range(len(runoff)):
            if runoff[i] < minValue and eliminated[i] == False:
                index = i
                minValue = runoff[i]
                
        eliminated[index] = True
        print("Run: %s " % runoff)
        print("Off: %s " % eliminated)
        print("Loser: %s" % index)
    except IOError:
        sys.exit("IOE Error: Fail to open %s !" % inputFile)
    else:
        file.close()

#main        
if __name__ == "__main__":

    count()
    
    for i in range(len(plural)):
        runoff.append(0)
        eliminated.append(False)
    for i in range(len(runoff)):
        eliminate()
    for i in range(len(eliminated)):
        if eliminated[i] == False:
            print("Winner: %s" % i)