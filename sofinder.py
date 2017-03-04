#!/usr/bin/env python
#coding:utf-8

''' 
This is a simple script to find a Share-Librarys(so) which has the symbol name you give in a Android device.
-i give the symbol name which is a import symbol in the so file to find;
-e give the symbol name which is a export symbol in the so file to find;
-a give the symbol name will find all so files which has the symbol name in it's symtab;
'''


import os 
import subprocess
from subprocess import call 
import shlex
from os import walk

import time
import os
import tempfile
import platform

class ADB:
    def __init__(self):
        # make sure we have adb
        if self._exec( "which adb" ) == "":
            raise "ADB binary not found in PATH."

    def push( self, src, dst ):
        self._exec( "adb push '%s' '%s'" % ( src, dst ), True )

    def pull(self, src, dst= '.'):
        self._exec( "adb pull '%s' '%s'" % (src,dst),True)

    def sh( self, cmd ):
        return self._exec( "adb shell '%s'" % cmd )

    def sudo( self, cmd ):
        return self.sh( "su -c \"%s\"" % cmd )

    def pkill( self, proc ):
        self.sudo( "pkill -9 %s" % proc )

    def clear_log( self ):
        self._exec( "adb logcat -c" )

    def set_selinux_level( self, level ):
        self.sh( "su 0 setenforce %d" % level )
        if level == 0:
            self.sh( 'su -c supolicy --live "allow s_untrusted_app shell_data_file file { execute execute_no_trans }"' )

    def get_pid( self, proc ):
        # print "proc = %s" % (proc)
        out = self.sudo( "ps | grep '%s'" % proc ).strip().split(' ')
        out = [x for x in out if x]
        pid = int( out[1] )
        return pid

    def start_activity( self, proc, activity ):
        self.pkill( proc )
        time.sleep(1)
        self.sh( "am start %s/%s" % ( proc, activity ) )
        return self.get_pid( proc )

    def logcat( self, tag = None ):
        if tag is not None:
            cmd = "adb logcat -s '%s'" % tag
        else:
            cmd = "adb logcat"

        proc = subprocess.Popen( cmd, stdout=subprocess.PIPE, shell=True )
        for line in iter( proc.stdout.readline, '' ):
            print line.rstrip()

    def _exec( self, cmdline, silent = False ):
        channel = open(os.devnull, 'wb') if silent is True else subprocess.PIPE
        p = subprocess.Popen( cmdline, stdout=channel, stderr=channel, shell=True )
        out, err = p.communicate()
        if err:
            print err
        if p.returncode != 0:
            print "[STDERR] : %s" % out

        return out



# or give your readelf's path
cmd_readelf = './bin/darwin/readelf'
root_dir = '/'


# don't traversal these blacklist path.
blacklist = ['/proc','/sys','/mnt/sdcard']
current_dir = root_dir
adb = ADB()

def loopAllFiles(dir):
    if dir in blacklist:
        return
    cmd = 'ls -l %s' % dir
    # print cmd
    for line in adb.sh(cmd).split('\n'):
        # print line
        if len(line)>0:
            if line.split()[0].startswith('d'): # DIR
                new_dir = '/'+line.split()[5] if dir=='/' else dir+'/'+line.split()[5]
                loopAllFiles(new_dir)
            elif (line.split()[0].startswith('-') and line.split()[6].endswith('.so')): # is it a so file?
                # print line.split()
                src_file = dir + '/' + line.split()[6]
                adb.pull(src_file,dest_file.name)
                # print 'need_find=%s' % need_find
                child1 = subprocess.Popen([cmd_readelf,"-Ws",dest_file.name], stdout=subprocess.PIPE)
                child2 = subprocess.Popen(["grep",need_find],stdin=child1.stdout, stdout=subprocess.PIPE)
                out = child2.communicate()[0]
                # print src_file
                # print dest_file.name
                # print out
                if len(out)>0:
                    print src_file # print the so path we needed.

def get_readelfcmd():
  operating_system = platform.system()
  cmd_folder = './bin/'
  if operating_system == 'Darwin':
    cmd_folder += 'darwin'
  elif operating_system == 'Linux': 
    cmd_folder += 'linux'
  elif operating_system == 'Windows':
    cmd_folder += 'linux' # not test on windows yet.   
  return  cmd_folder+'/readelf' 

def get_args_parser():
  import argparse
  from argparse import RawTextHelpFormatter
  desc = 'Uses sofinder to find a Share-Librarys(so) which has the symbol name you give in a Android device.'
  p = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
  p.add_argument('--impor', '-i', type=str,
                help='A symbol name which is a import symbol in the so file to find.')
  p.add_argument('--export', '-e', type=str,
                help='A symbol name which is a export symbol in the so file to find.')
  p.add_argument('--all', '-a', type=str,
                help='A the symbol name will find all so files which has the symbol name in its symtab')
  return p


def do_process(symbol):
  global need_find
  need_find = symbol
  cmd_readelf = get_readelfcmd()
  global dest_file
  dest_file = tempfile.NamedTemporaryFile()
  loopAllFiles(current_dir)
  dest_file.close()


def main():
  parser = get_args_parser()
  args = parser.parse_args()
  if args.impor != None:
    symbol = 'UND ' + args.impor.strip()
  elif args.export != None:
    symbol = '[[:digit:]] '+ args.export.strip()
  elif args.all != None:
    symbol = args.all.strip()

  do_process(symbol)  


if __name__ == '__main__':
    main()







