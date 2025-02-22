import os
from shortwalk import walk
from bashrange import expand_args
import asyncio
from .parse import parse_args
from .node import expr_to_pred
from .alg import walk_all

def print_help():
    print("""usage: pyfind [PATHS] [OPTIONS] [PREDICATES] [ACTION]

finds files and dirs that satisfy predicates and executes action

options:
  -maxdepth NUMBER     walk no deeper than NUMBER levels
  -output PATH         output to file instead of stdout
  -append              append to file instead of rewrite
  -trail               print trailing slash on directories
  -cdup NUMBER         print (or perform action on) parent path (strip NUMBER 
                       trailing components from path)
  -first NUMBER        print (or perform action on) first NUMBER found items and stop
  -skip PATTERNS       do not go into dirs with name that matches one of PATTERNS (wildcard) 
                       and do not act on files with name that matches one of PATTERNS

predicates:
  -type d              is directory
  -type f              is file
  -mtime DAYS          if DAYS is negative: modified within DAYS days, 
                       if positive modified more than DAYS days ago
  -ctime DAYS          same as -mtime, but when modified metadata not content
  -mmin MINUTES        if MINUTES is negative: modified within MINUTES minutes, 
                       if positive modified more than MINUTES minutes ago
  -mdate DATE1 [DATE2] modified at DATE1 (or between DATE1 and DATE2)
  -cmin MINUTES        same as -mmin, but when modified metadata not content
  -newer PATH/TO/FILE  modified later than PATH/TO/FILE
  -newermt DATETIME    modified later than DATETIME
  -newerct DATETIME    same as -newermt but when modified metadata not content
  -name PATTERNS       filename matches one of PATTERNS (wildcard)
  -iname PATTERNS      same as -name but case insensitive
  -path PATTERNS       file path matches one of PATTERNS (wildcard)
  -ipath PATTERNS      same as -path but case insensitive
  -grep PATTERN        file content contains one of PATTERNS (regexp)
  -igrep PATTERN       same as -grep but case insensitive
  -bgrep PATTERN       same as -grep but PATTERN is string of hex values
  -docgrep PATTERN     grep odt and ods files for PATTERN
  -xlgrep ...ARGS      grep xls files for values, each arg is one of: address range (c1:c10), 
                       numeric value (40.8), numeric range (40..41) or string (foo)
  -cpptmp              temporary cpp files (build artifacts - objects, generated code)
  -zippath PATTERNS    zip containing file with path that matches one of PATTERNS (wildcard)
  -zipipath PATTERNS   same as -zippath but PATTERNS are case insensitive
  -dirwith PATTERNS    directory contains entry with name that matches one of PATTERNS (wildcard)
  -dirwithf PATTERNS   directory contains file with name that matches one of PATTERNS (wildcard)
  -dirwithd PATTERNS   directory contains subdirectory with name that matches one of PATTERNS (wildcard)
  -video               video files (*.mkv *.mp4 *.mov *.webm *.flv *.avi *.mpg *.mpeg *.wmv)
  -image               image files (*.jpg *.jpeg *.png *.gif *.webp *.svg *.bmp *.ico *.tif *.tiff)

predicates can be inverted using -not, can be grouped together in boolean expressions 
using -or and -and and parenthesis
          
actions:
  -print               print matched paths to output (default action)
  -delete              delete matched file
  -exec COMMAND ;      execute COMMAND
  -touch               touch file (set mtime to current time)
  -gitstat             print git status summary
  -extstat             filesize and filecount stat by file extension
  -copy DST            copy file to DST
  -move DST            move file to DST 

print action options:
  -abspath             print absolute paths
  -basename            print basename
  -stat                print paths with file size and modification date

exec action options:
  -async               execute asyncronously (do not wait for termination)
  -xargs               execute command once with all matched files as arguments
  -conc NUMBER         concurrency limit for -async -exec, 
                       defaults to number of cpu cores

exec action bindings:
  {}          path to file
  {path}      path to file
  {name}      name with extension
  {ext}       extension
  {basename}  name without extension
  {dirname}   directory name

copy and move action options:
  -tree                copy (move) preserving relative path (default)
  -flat                copy (move) without preserving relative path
  -noover              do not overwrite existing files (files are compared by size and name)
  -rename              rename files to avoid overwriting existing files

examples:
  pyfind -iname *.py -mmin -10
  pyfind -iname *.cpp *.h -not ( -iname moc_* ui_* ) -xargs -exec pywc -l ;
  pyfind -iname *.h -exec pygrep -H class {} ;
  pyfind -iname *.o -delete
  pyfind D:\\dev -iname node_modules -type d -cdup 1
  pyfind -iname *.dll -cdup 1 -abspath | pysetpath -o env.bat
  pyfind -iname *.mp3 -conc 4 -async -exec ffmpeg -i {} {dirname}\\{basename}.wav ;
  pyfind -mdate 2024-07-25
  pyfind -mdate 2024-07-25 2024-08-21
  pyfind -newer path/to/file
  pyfind D:\\dev -maxdepth 1 -gitstat
  pyfind D:\\dev -dirwith __init__.py
  pyfind D:\\dl -extstat
  pyfind C:\\Qt\\6.7.1 -iname *.dll -bgrep "5571feff"
  pyfind D:\\doc -xlgrep c1:c10 30.8 40..41 foo
  pyfind -iname *.txt -xargs -exec 7z a texts.zip ;
  pyfind -zipipath *.mtl
  pyfind D:\\dl -image -copy E:\\backup\\dl -noover
  pyfind D:\\dev\\blog -skip .git node_modules -mtime -10 -stat
""")

async def async_main():

    args = expand_args()

    debug = False
    if len(args) > 0 and args[-1] == '-debug':
        args.pop(-1)
        debug = True
    
    if len(args) > 0 and args[-1] in ['-h', '--help']:
        print_help()
        return

    expr, paths, action, extraArgs = parse_args(args)

    if debug:
        print(expr); exit(0)

    tree, pred = expr_to_pred(expr)

    if len(paths) == 0:
        paths.append(".")
    
    walk_all(paths, pred, action, extraArgs)

    await action.wait()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()