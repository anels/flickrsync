import glob
import os
import hashlib
import time
import subprocess

COMMENT_CHAR = '#'
OPTION_CHAR =  '='

def parse_config(filename):
  options = {}
  f = open(filename)
  for line in f:
    # First, remove comments:
    if COMMENT_CHAR in line:
      # split on comment char, keep only the part before
      line, comment = line.split(COMMENT_CHAR, 1)
    # Second, find lines with an option=value:
    if OPTION_CHAR in line:
      # split on option char:
      option, value = line.split(OPTION_CHAR, 1)
      # strip spaces:
      option = option.strip()
      value = value.strip()
      # store in dictionary:
      options[option] = value
  f.close()
  return options

def md5Checksum(filePath):
  with open(filePath, 'rb') as fh:
    m = hashlib.md5()
    while True:
      data = fh.read(8192)
      if not data:
        break
      m.update(data)
    return m.hexdigest()



# Step 1: read config
target_dir = "/home/anels/Dropbox/Camera Uploads"
md5_file = ""
freq = 60
if os.path.isfile("config.ini"):
  print 'Config file exists!'
  options = parse_config('config.ini')
  print options
  target_dir = options['target_dir']
  md5_file = options['md5_file']
  freq = options['freq']
else:
  print 'Config file does not exist! Using default settings.'

print target_dir
print md5_file
print freq

# Step 2: read md5 file
if os.path.isfile(md5_file):
  print 'md5_file is exist!'
  file = open(md5_file, "r")
  lines = file.readlines()
  file.close()
else:
  print 'md5_file is not exist! creating it...'
  lines = []

ext_list = ['gif','jpg','jpeg','png'];

# Step 3: monitor target dir
while(1):
  for target_file in glob.glob(os.path.join(target_dir, "*.*")):
    print target_file,
    if target_file.rsplit('.',1)[1] in ext_list :
      md5 = md5Checksum(target_file)
      print '\tThe MD5 checksum: ', md5,
      if any(md5 in s for s in lines):
        print "check"
      else:
        print "new!"
        file = open(md5_file, "a")
        file.write(md5)
        file.write("\n")
        file.close()
        lines.append(md5)
        subprocess.call(["flickr_upload", target_file])
    else:
      print '...ignored'
  print 'sleep '+freq + ' secs.'
  time.sleep(float(freq))



# list all files recursively
#for root, dirs, files in os.walk("/"):
#    for file in files:
#        if file.endswith(".txt"):
#             print os.path.join(root, file)
