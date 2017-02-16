# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:40:54 2016

@author: jlee

TODO======================
create gui for easy file/folder selection
change the way I iterate through loops
allow list to be written to the csv if the spacing is off
==========================


"""

import os, sys
import re, csv, time, datetime

#fileName = str("C:\Users\jlee\Documents\76243 - GPS Availability at MEXCAN\ES034\MMSI_LOG_0317b.txt")
line = ""
counter = 0
fileListPath    = []
fileListName    = []
session_name    = "session_1" #each session may contain multiple files
csv_fname       = "cvs_output.csv"
time_flag       = False
path = sys.argv[1]
tagList = ['RE00D', 'RE00B', 'RE029', 'GPGGA', 'LOAD','DL02C']
csv_col_head = ['id', 'timedate', 'time', 'date', 'time_delta'                  #datetime
                'ext', 'board', 'backup', 'd3v', 'a3v', 'd5v', 'a5v', 'd2_5',   #voltage
                'utc','lat','lathead','long','longhead','fix','sats','hdop','alt','alt_unit','height','height_unit','IDK','chcksum',    ##GPGGA
                'cpu_load',
                'DL_ID','Decoder_ID','Ref_Station_ID','Time_Last_Msg','NumOfRec_Msg','NumOfCorrupt_Msg','DL_Quality']

class Raw_Log:
    def __init__(self, session):
        self.session_name = session
        self.file_list_path = []
        self.file_list_name = []
        self.file_list_cpu_path = []
        self.file_list_cpu_name = []
    def get_meta_file_data(self):
        for dirName, subdirlList, fileListTemp in os.walk(path, topdown=False):
            print('Found directory: %s' % dirName)
            for fname in fileListTemp:
                print('\tfname = %s' % fname)
                print('\t\t%s' % os.path.join(dirName, fname))
                tempFile = os.path.join(dirName, fname)
                if "tps" in tempFile or "cpulog" in tempFile:
                    self.file_list_path.append(tempFile)
                    self.file_list_name.append(fname)

    def order_files(self):
        #we assume that the file lists are in reverse order ie bb, ba, b
        comp_file_name_0 = re.search('\d([a-z]+)\.tps', self.file_list_name[0])
        comp_file_name_1 = re.search('\d([a-z]+)\.tps', self.file_list_name[1])
        if comp_file_name_1.group(1) > comp_file_name_0.group(1):  #if list goes from a to z
            self.file_list_name.reverse()
            self.file_list_path.reverse()

    def parse_raw_log(self):
        file_counter = 0
        for i in range(len(self.file_list_path)): #self.file_list_name)):
            time_flag = False   #this makes sure that time is the very first entry
            with open(self.file_list_path.pop(), "rb") as file:
                for line in file:
                    if "cpulog" in file: cpu_log.parse_cpu_ptx()
                    for tag in tagList:
                        matchTag = re.search(tag, line)
                        if matchTag == None : continue
                        if matchTag.group() == tagList[0]:
                            time_log.parse_time(line)
                            time_flag = True
                            break
                        if time_flag == False: break
                        if matchTag.group() == tagList[1]:
                            time_log.parse_date(line)
                            break
                        if matchTag.group() == tagList[2]:
                            volt_log.parse_volt(line)
                            break
                        if matchTag.group() == tagList[3]:
                            gps_log.parse_gps(line)
                            break
                        if matchTag.group() == tagList[4]:
                            cpu_log.parse_cpu(line)
                            break
                        if matchTag.group() == tagList[5]:
                            gps_log.parse_gps_dl(line)
                            break
#=========C S V    N O - C L A S S================================
def add_to_csv2(csv_fname2):
    csv.register_dialect('dialect01', delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ', lineterminator="\n",
                     doublequote=False)
    with open(csv_fname2, 'w') as cvs_f:
        # writer = csv.writer(cvs_f, delimiter=',', dialect="dialect01", lineterminator="\n")
        writer = csv.writer(cvs_f, 'dialect01')
        writer.writerow(csv_col_head)
        for i in range(len(gps_log.list_gps_dl)):
            writer.writerow( (i+1, time_log.list_timedate[i], time_log.list_time[i], time_log.list_date[i], time_log.list_timedelta[i],
                              volt_log.list_volt[i],
                              gps_log.list_gps[i],
                              cpu_log.list_cpu[i],
                              gps_log.list_gps_dl[i]) )
#=========C S V    C L A S S======================================
# csv.register_dialect('dialect01', delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
#                      doublequote=False)

class CSV:
    def __init__(self, cvs_fname):        self.fname = cvs_fname
    def add_to_csv(self):
        with open(self.fname, 'w') as cvs_f:
            pass
class Time:
    def __init__(self, session):
        self.time_session = session
        self.list_time = []
        self.list_date = []
        self.list_timedate = []
        self.list_timedelta = []
        #self.line = line
    def parse_time(self, line):
        new_time = line.split(' ')
        new_time = new_time[1].split('.')
        self.list_time.append(new_time[0])
    def parse_date(self, line):
        line = line[6:-2]    #remove the newline and tag
        line.rstrip()
        # line = time.strptime(line, "%y %d %b")
        self.list_date.append(line)
        pass
class Volt:
    def __init__(self, session):
        self.volt_session = session
        self.list_volt = []
        self.ext = []
        self.board = []
        self.backup = []
        self.d3v = []
        self.a3v = []
        self.d5v = []
        self.a5v = []
        self.d2_5v = []
        self.d1_5v = []
        self.d1_2v = []
        volt_list_of_list = []
        volt_list_of_list.append(self.volt_session)
        volt_list_of_list.append(self.ext)
        volt_list_of_list.append(self.board)
        volt_list_of_list.append(self.backup)
        print volt_list_of_list
    def parse_volt(self, line):
        temp_volt = line.split('{')
        temp_volt = temp_volt[1].rstrip()
        temp_volt = temp_volt[:-1]  #remove last curly brace
        self.list_volt.append(temp_volt)
class GPS:
    def __init__(self,session):
        self.gps_session = session
        self.list_gps = []
        self.list_gps_dl = []
    def parse_gps(self, line):
        temp_gps = line.split('A,')
        temp_gps = temp_gps[1].rstrip()
        self.list_gps.append(temp_gps)
    def parse_gps_dl(self, line):
        temp_gps = re.search('{(\S+)}',line)
        self.list_gps_dl.append(temp_gps.group(1))
class CPU:
    def __init__(self, session):
        self.cpu_session = session
        self.list_cpu = []
        self.list_cpu_ptx = []
    def parse_cpu(self,line):
        temp_cpu = re.search('LOAD,(\d+)', line)
        # print temp_cpu.group(1)
        cpu_log.list_cpu.append(temp_cpu.group(1))
    def parse_cpu_ptx(self):
        index = Raw_Log.file_list_name("cpulog.txt")
        with open(Raw_Log.file_list_path[index]) as file:
            for line in file:
                if "Application.exe" in line:
                    pid = re.search('NAME: (\S+)\s+Threads\s+(\d+)\s+CPU:\s+(\d+)',line)

                if "CPU @" in line:
                    cpu_tot = re.search('CPU @ (\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)\s+(\w+):\s(\d+.\d+)\s+'
                                        'Min:\s+(\d+.\d+)\s+'
                                        'Max:\s+(\d+.\d+)\s+'
                                        'Avg:\s+(\d+.\d+)\s+'
                                        'Avg:\s+(\d+.\d+)')
                    #convert the AM/PM time to 24HR time

                    temp_cpu_time = datetime.datetime( int(cpu_tot.group(1)), int(cpu_tot.group(2)), int(cpu_tot.group(3)),
                                                       )

            #add data to list



def create_datetime():
    for i in range(len(time_log.list_time)):
        # print time_log.list_date[i].split('-')
        date =  re.search('^(\d+)-(\d+)-(\d+)', time_log.list_date[i])
        time = re.search('^(\d+):(\d+):(\d+)', time_log.list_time[i])
        temp_time = datetime.datetime( int(date.group(1)),int(date.group(2)),int(date.group(3)),int(time.group(1)),int(time.group(2)),int(time.group(3)) )
        time_log.list_timedate.append(temp_time)
        #sneak in the time_delta :)
        if i == 0: continue
        time_delta = time_log.list_timedate[i] - time_log.list_timedate[i-1]
        time_log.list_timedelta.append(time_delta)


# def create datetime_1(line, list):  #this one is more generic than orig. it prevents create extra, unnecessary lists
#     temp_datetime = Time()
#     # i need to pass it the class.list it will belong to you.
#     return


if __name__ == "__main__":
    start = time.time()
    time_log = Time(session_name)
    volt_log = Volt(session_name)
    gps_log = GPS(session_name)
    cpu_log = CPU(session_name)
    session_1 = Raw_Log(session_name)
    session_1.get_meta_file_data()
    if len(session_1.file_list_path ) > 1 : session_1.order_files()
    session_1.parse_raw_log()
    create_datetime()

    #call the CSV shit to write a CSV now that we have the Lists
    add_to_csv2("test.csv")
    end = time.time()
    print (end-start)
