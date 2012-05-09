import sys

def svn_split_name(svnurl):
    print svnurl.split('/')[-2]        

if __name__ == '__main__':
    svn_split_name(sys.argv[1])
