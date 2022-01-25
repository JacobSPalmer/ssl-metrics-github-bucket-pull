import subprocess
from datetime import datetime
import os
import progress_win_patch
progress = progress_win_patch.getpatchedprogress()
from progress.bar import Bar

##How To Use
#1. Put bucket-pull.py & progress_win_patch.py into a folder
#1. In the same folder, copy/Paste GitHub Token into a text file named "token.txt"
#2. copy/Paste the URLs of the repositories to bucket pull into a txt file named "repo_list.txt"
#4. Run the bucket-pull.py in CLI or in an IDE


##Required Packages
#progress
#ssl-metrics-github-issues


##Read in environment token

with open('token.txt') as TOKEN:
    token = TOKEN.readline()

##Read in and prep the repo list

with open('repo_list.txt') as REPOS:
    repo_list = REPOS.readlines()

##Remove duplicate repos
repo_list = list(set(repo_list))

##Template Command
comm_template = "ssl-metrics-github-issues-collect -r {} -t {} -s {}"
comm_list = []

##Generate the commands
for repo in repo_list:
    repo = repo.strip()
    if repo[-1] == '/':
        repo = repo[:-1]
    repo_owner, repo_name = repo.split("/")[-2], repo.split("/")[-1]
    owner_name = repo_owner + "/" + repo_name
    date = datetime.today().strftime('%Y-%m-%d')
    json_name = repo_owner + "_" + repo_name + "_" + date + ".json"
    comm = comm_template.format(owner_name, token, json_name)
    comm_list.append(comm)

##Check/create directories to store the bucket pull

if not os.path.isdir(os.getcwd() + "/Repos/"):
    os.makedirs(os.getcwd() + "/Repos")

if not os.path.isdir(os.getcwd() + "/Repos/" + str(datetime.today().strftime('%Y-%m-%d'))):
    os.makedirs(os.getcwd() + "/Repos/" + datetime.today().strftime('%Y-%m-%d'))

##Save a list of all repos within the folder
path_name = os.getcwd() + "/Repos/" + datetime.today().strftime('%Y-%m-%d')
with open(path_name + "/" + "repos-pulled-{}.txt".format(str(datetime.today().strftime('%Y-%m-%d'))), "w") as output:
    for comm in comm_list:
        s = comm.split(" ")[-5]
        output.write(s+'\n')

##Run the commands to pull each repo in repo_list.txt
with Bar('Incremental Bar', max = len(comm_list)) as Bar :
    for command in comm_list:
        if not os.path.exists(path_name + "/" + command.split(" ")[-1]):
            subprocess.call(command, shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT,
                            cwd=path_name)
        Bar.next()
    Bar.finish()
    print("Bucket Pull Complete")









