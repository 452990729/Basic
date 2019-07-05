#!/usr/bin/env python2

import sys
import os
import re
import time
import subprocess


def GetJobID(cmd_in):
    assert isinstance(cmd_in, str), 'The Job Comand is not string'
    a = os.popen('ps x')
    JobAll = a.read().split('\n')
    m = 0
    pid = 0
    for line in JobAll:
        if re.search(cmd_in, line):
            pid = re.split('\s+', line.strip())[0]
    return pid

def GetAllJobs():
    a = os.popen('ps x')
    JobAll = a.read().split('\n')
    AllJob = []
    for line in JobAll:
        pid = re.split('\s+', line.strip())[0]
        AllJob.append(pid)
    return AllJob

def GetRestJobs(job_list):
    assert isinstance(job_list, list), 'The Job list is not a list'
    AllJob = GetAllJobs()
    RestJob = []
    for job in job_list:
        if job in AllJob:
            RestJob.append(job)
    print "Still Waiting on  {} jobs...".format(len(RestJob))
    return RestJob

def WaitOnJobs(cmd_list, delay=30, num=4, special_interp='sh'):
    assert isinstance(cmd_list, list), 'The Cmd list is not a list'
    i = 0
    job_list = []
    print "Waiting on  {} jobs...".format(len(cmd_list))
    curr_time = time.strftime("%x, %X")
    print "  - Starting to wait at {}".format(curr_time)
    for cmd in cmd_list:
        i += 1
        if i <= num:
            os.popen('nohup {} {} 1>{}.o 2>{}.e&'.format(special_interp, cmd, cmd, cmd))
            job_list.append(GetJobID(cmd))
        else:
            while 1:
                RestJob = GetRestJobs(job_list)
                print RestJob
                Res = num-len(RestJob)
                if Res:
                    os.popen('nohup {} {} 1>{}.o 2>{}.e&'.format(special_interp, cmd, cmd, cmd))
                    job_list.append(GetJobID(cmd))
                    i = i-Res+1
                    break
                else:
                    time.sleep(delay)
    while len(GetRestJobs(job_list)):
        time.sleep(delay)

def LaunchJobs(cmd_list, delay=30, num=4, special_interp='sh'):
    job_list = []
    if isinstance(cmd_list,list):
        pass
    elif isinstance(cmd_list,str):
        cmd_list = [cmd_list]
    else:
        sys.exit('wrong cmd line !')
    WaitOnJobs(cmd_list, delay, num, special_interp)


