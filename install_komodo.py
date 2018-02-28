#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  install_comodo.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import os
import pwd
import subprocess
import urllib
from bs4 import BeautifulSoup




def check_package(package):
    if subprocess.call("rpm -q {} >/dev/null".format(package),shell=True)==0:
        return True
    return False
    
def install_package():
    packages = ["gtk+", "glib2", "pango", "libstdc++", "gdk-pixbuf2",\
 "libgnome", "libgnomeui", "scim", "scim-gtk", "scim-bridge-qt3"]
    packages = [package for package in packages if not check_package(package)]
    if packages:
        packages = " ".join([package for package in packages])
    else:
        return True
    
    if subprocess.call("pkexec dnf install -y --best  "+packages,shell=True)!=0:
        print("Install '{}' Fail.\n".format(packages))
        return False
    else:
        return True

def get_komodo_downlaod_link():
    if os.uname().machine == "x86_64":
        download_arch = "linuxx86_64"
    else:
        download_arch = "linuxx86"
    
    url = urllib.request.Request("https://www.activestate.com/komodo-ide/downloads/edit",headers={"User-Agent":"Mozilla/5.0"})
    try:
        htmldoc = urllib.request.urlopen(url,timeout=10)
    except Exception as e:
        print(e)
        return False
    soup = BeautifulSoup(htmldoc.read(),"html.parser")
    for tag in soup.findAll("td",{"class":"dl_link"}):
        try:
            if tag.a.attrs["data-platform"] == download_arch:
                return tag.a.attrs["href"].split("=",1)[-1]
        except:
            continue
    return False



def downlaod_komodo(link):
    try:
        url   = urllib.request.Request(link,headers={"User-Agent":"Mozilla/5.0"})
        opurl = urllib.request.urlopen(url,timeout=10)
        try:
            saveas = os.path.join(os.getcwd(),opurl.headers["Content-Disposition"].split("=",1)[-1])
        except :
            saveas = os.path.join(os.getcwd(),os.path.basename(opurl.url))
            
        if  os.path.isfile(saveas):
            while True:
                print ("{} Is Exists\n\nF To Force ReDownload || S To Skip Redownload || Q To Exit :".format(saveas))
                answer = input("- ")
                if answer == "q" or answer == "Q":
                    exit("\nbye...\n")
                elif answer == "S" or answer == "s":
                    return saveas
                elif answer == "F" or answer == "f":
                    #subprocess.call("rm {}".format(saveas),shell=True)
                    break
        size = int(opurl.headers["Content-Length"])
        psize = 0
        print ("["+"-"*80+"]"+" "+str(size)+"b"+" "+"0%",end="\r",flush=True)
        with open(saveas, 'wb') as op:
            while True:
                chunk = opurl.read(600)
                if not chunk:
                    break
                count = int((psize*80)//size)
                n = "#" * count
                fraction = count/80
                op.write(chunk)
                psize += 600
                print ("["+n+"-"*(80-count)+"]"+" "+str(size)+"b"+" "+str(round((psize*80)/size,2))+"%",end="\r",flush=True)
        print (" "*200,end="\r",flush=True)
        print ("["+"#"*80+"]"+" "+str(size)+"b"+" "+"100%")
    except Exception as e:
        print(e)
        return False
        
    return saveas
            

def install_komodo(location):
    if subprocess.call("tar -xvzf {} -C /tmp".format(location),shell=True) != 0:
        return False
    folder_name = os.path.basename(location).rsplit(".",2)[0]
    install_location = os.path.join(pwd.getpwuid(os.geteuid()).pw_dir,folder_name)
    install_file_location = os.path.join("/tmp",folder_name)
    old_cwd = os.getcwd()
    os.chdir(install_file_location)
    if subprocess.call("./install.sh -I {}".format(install_location),shell=True) != 0 :
        return False
    os.chdir(old_cwd)
    
    os.makedirs(os.path.join(pwd.getpwuid(os.geteuid()).pw_dir,"bin"),exist_ok=True)
    subprocess.call("ln -sf {} {}".format(os.path.join(install_location,"bin","komodo"),os.path.join(pwd.getpwuid(os.geteuid()).pw_dir,"bin","komodo")),shell=True)
    return True
     

    


def main():
    if not install_package():
        exit(1)
        
    link = get_komodo_downlaod_link()
    if not link :
        print("\nGet Download Link Fail.")
        exit(1)
    
    install_file_location = downlaod_komodo(link)
    if not install_file_location:
        print("\nDownload Install File Fail.")
        exit(1)
    
    install = install_komodo(install_file_location)
    if not install:
        print("\nInstall Komodo Fail.")
        exit(1)
    
    print("\nInstall Success.")
    exit(0)
if __name__ == "__main__":
    main()





















