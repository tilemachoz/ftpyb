#!/usr/bin/env python

#
# A small python script for ftp back
# ease and automtation. All included 
# one file to ease cron scheduling.
# 
# Copyright (c) 2016, Tilemachos B.
# 

from ftplib import FTP
import os


class Backup:
	"""
	A class that is used for the back up from 
	the ftp server.
	"""
	
    def get_all_files(self, filenames):
		"""
		A recursive method that downloads everything
		under a specified directory.
		"""
        for filename in filenames:
            if filename[1]['type'] == 'file':
                self.get_file(filename[0], ftp.pwd())
                continue
            if filename[1]['type'] == 'dir':
                ftp.cwd(filename[0])
                self.get_all_files(ftp.mlsd())
                ftp.cwd('..')
                continue

    def get_file(self, filename, d):
		"""
		A method that downloads a file in a specific 
		directory path.
		"""
        local_file = "backup" + d + "/" + filename
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        f = open(local_file, "wb")
        ftp.retrbinary('RETR %s' % filename, f.write)
        f.close
        return


class Automate:
	"""
	A class that produce a python script for a 
	specific backup task that needs to be automated.
	"""
	
    back = Backup()
    host = ''
    user = ''
    password = ''
    path = ''
    bckup_filename = ''
    
    
    def create_backup_script(self):
		"""
		A method that writes the code needed in a file
		using the specified user input
		"""
		
        code = "from ftplib import FTP\n" \
                "import os\n" \
                "\n" \
                "ftp=FTP('%(host)s')\n" \
                "ftp.login('%(user)s','%(pass)s')\n" \
                "ftp.cwd('%(path)s')\n" \
                "\n" \
                "def get_all_files(filenames):\n" \
                "    for filename in filenames:\n" \
                "        if filename[1]['type'] == 'file':\n" \
                "            get_file(filename[0], ftp.pwd())\n" \
                "            continue\n" \
                "\n" \
                "        if filename[1]['type'] == 'dir':\n" \
                "            ftp.cwd(filename[0])\n" \
                "            get_all_files(ftp.mlsd())\n" \
                "            ftp.cwd('..')\n" \
                "            continue\n" \
                "\n" \
                "\n" \
                "def get_file(filename, d):\n" \
                "    local_file = 'backup' + d + '/' + filename\n" \
                "    os.makedirs(os.path.dirname(local_file), exist_ok=True)\n" \
                "    f = open(local_file, 'wb')\n" \
                "    ftp.retrbinary('RETR %%s' %% filename, f.write)\n" \
                "    f.close\n" \
                "    return\n" \
                "\n" \
                "\n" \
                "get_all_files(ftp.mlsd())\n" % {'host': self.host, 'user': self.user, 'pass': self.password, 'path': self.path}

        script_file = self.bckup_filename + ".py"
        f = open(script_file, 'w')        
        print(code, file=f)
        pass
    
    def get_user_input(self):
		"""
		A method in which the user specifies the parameters for the automation script
		"""
        print('*** Starting the input process of ftp back up python script creation. *** \n')
        self.host = input('What is the hostname? ')
        self.user = input('What is the username? ')
        print('NOTE! Your password will travel in simple text through ftp protocol.')
        self.password = input('What is the password? ')
        self.path = input('What is the path of the directory you want to back up? ')        
        self.bckup_filename = input('What will be the filename of your back up file? ')
        pass

    def main(self):
		"""
		Main method of the class is the only who 
		is called by obj.
		"""
        self.get_user_input()
        self.create_backup_script()
        pass

class UI:
	"""
	The class that produces the User Interface either for live
	ftp back up or automated script production
	"""
    backup = Backup()

    def directory_listing(self):
        return ftp.dir()

    def current_path(self):
        print(ftp.pwd())
        pass

    def move_to_dir(self, path):
        return ftp.cwd(path)

    def error(self):
        print("This Command not found try `help` command.")
        pass

    def quit(self):
        return ftp.quit()

    def help(self):
        print("""
        ls			Direcotry Listing
        pwd			Current Path
        cd			Move to directory <path>
        help		Prints this page
        getf		Download a file from current directory <filename>
        getd		Download a directory and all its contents <directory>
        exit		Leave the ftp server and the script
        connect		Connect to the ftp server <host>
        login		Login to ftp with credentials given <user@password>
        automate	Begins process for creation of automated script
        """)
        pass

    def get_file(self, filename):
        return self.backup.get_file(filename, ftp.pwd())

    def get_directory(self, directory):
        self.move_to_dir(directory)
        return self.backup.get_all_files(ftp.mlsd())

    def connect(self, host):
        global ftp
        ftp = FTP(host)
        pass

    def auto(self):
        auto = Automate()
        auto.main()
        pass

    def login(self, credentials):
        cred = credentials.split('@')
        return ftp.login(cred[0], cred[1])

    def get_file(self, filename):
        return self.backup.get_file(filename, ftp.pwd())

    def command(self, cmd, arg=''):
		"""
		Method that maps user input to actual commands
		"""
        if cmd == 'ls':
            return self.directory_listing()
        elif cmd == 'pwd':
            return self.current_path()
        elif cmd == 'cd':
            return self.move_to_dir(arg)
        elif cmd == 'help':
            return self.help()
        elif cmd == 'getf':
            return self.get_file(arg)
        elif cmd == 'getd':
            return self.get_directory(arg)
        elif cmd == 'exit':
            return self.quit()
        elif cmd == 'connect':
            return self.connect(arg)
        elif cmd == 'user':					# deprecated
            return self.user(arg)
        elif cmd == 'login':
            return self.login(arg)
        elif cmd == 'automate':
            return self.auto()            
        else:
            return self.error()


ui = UI()
cmd = ""
while cmd != 'exit':
    cmd = input(">> ")
    lcmd = cmd.split()
    ui.command(lcmd[0], lcmd[1]) if len(lcmd) == 2 else ui.command(lcmd[0])



