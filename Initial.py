import git
import os, fnmatch
from pathlib import Path
import sys
import time

repo_link = sys.argv[1]  # Taking the argument 'Repo Link' from command line
extenstion = sys.argv[2]  # Taking the argument 'Extension' from command line
name_of_lang = sys.argv[3]  # Taking the argument 'Name of the language' from command line
out1_name = sys.argv[4]  # Taking the argument 'output1' from command line
out2_name = sys.argv[5]  # Taking the argument 'output2' from command line

git.Repo.clone_from(sys.argv[1], 'paths'+str(time.time()))
dir_list = os.listdir('paths')
python_paths, golang_paths, javascript_paths, rubylang_paths = list(), list(), list(), list()

for directories, folders, files in os.walk(r'paths'):
    for file in files:
        if file.find(".py") > 0:
            python_paths.append(os.path.join(directories, file))
        if file.find(".go") > 0:
            golang_paths.append(os.path.join(directories, file))
        if file.find(".js") > 0:
            javascript_paths.append(os.path.join(directories, file))
        if file.find(".rb") > 0:
            rubylang_paths.append(os.path.join(directories, file))

from tree_sitter import Language, Parser

Language.build_library(
  'build/my-languages.so',
  [
    'tree-sitter-go-master',
    'tree-sitter-javascript-master',
    'tree-sitter-python-master',
    'tree-sitter-ruby-master',
  ]
)

GO_LANGUAGE = Language('build/my-languages.so', 'go')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
PY_LANGUAGE = Language('build/my-languages.so', 'python')
RB_LANGUAGE = Language('build/my-languages.so', 'ruby')

python_parser = Parser()
python_parser.set_language(PY_LANGUAGE)

js_parser = Parser()
js_parser.set_language(JS_LANGUAGE)

go_parser = Parser()
go_parser.set_language(PY_LANGUAGE)

ruby_parser=Parser()
ruby_parser.set_language(RB_LANGUAGE)

source_code_check = '''
a = 10
b = 20
c = a + b
print(c)
'''

def list_of_identifiers(source, parser):
  final_list_identifiers = []

  def parsing(code):
    if (len(code.children) == 0):
      return
    else:
      for i in code.children:
        if (i.type == 'identifier'):
          final_list_identifiers.append(i)
        parsing(i)

  parsed_tree = parser.parse(bytes(source, "utf8"))

  root_node = parsed_tree.root_node
  parsing(root_node)
  return final_list_identifiers

python_programs, python_codes = list(), list()
#print(python_paths)

#for i in range(len(python_paths)):
 #   print(python_paths[i])

sys.stdout = open(sys.argv[4], "w")

if extenstion == '.py' and name_of_lang == 'python':
    for i in range(len(python_paths)):
        with open(python_paths[i]) as f:
            contents = f.read()
            #python_programs.append(python_paths[i].split('\\')[-1])
            #python_codes.append(contents)
            ids = list_of_identifiers(contents, python_parser)
            #print(contents)
            #print(ids)
            contents = contents.split('\n')
            print('\n')
            print("output1 for", python_paths[i].split('\\')[-1])
            for node in ids:
                print("identifier-",contents[node.start_point[0]][node.start_point[1]:node.end_point[1]],"at Row no",node.start_point[0],"Col No",node.start_point[1])
        print('-----------------------------------------------------------------------------------')

elif extenstion == '.go' and name_of_lang == 'go':
    for i in range(len(golang_paths)):
        with open(golang_paths[i]) as f:
            contents = f.read()
            #python_programs.append(python_paths[i].split('\\')[-1])
            #python_codes.append(contents)
            ids = list_of_identifiers(contents, go_parser)
            #print(contents)
            #print(ids)
            contents = contents.split('\n')
            print('\n')
            print("output1 for", golang_paths[i].split('\\')[-1])
            for node in ids:
                print("identifier-",contents[node.start_point[0]][node.start_point[1]:node.end_point[1]],"at Row no",node.start_point[0],"Col No",node.start_point[1])
        print('-----------------------------------------------------------------------------------')

elif extenstion == '.js' and name_of_lang == 'javascript':
    for i in range(len(javascript_paths)):
        with open(javascript_paths[i]) as f:
            contents = f.read()
            #python_programs.append(python_paths[i].split('\\')[-1])
            #python_codes.append(contents)
            ids = list_of_identifiers(contents, js_parser)
            contents=contents.split('\n')
            print('\n')
            print("output1 for", javascript_paths[i].split('\\')[-1])
            for node in ids:
                print("identifier-",contents[node.start_point[0]][node.start_point[1]:node.end_point[1]],"at Row no",node.start_point[0],"Col No",node.start_point[1])
        print('-----------------------------------------------------------------------------------')

else:
    print("invalid input")

for i in range(len(rubylang_paths)):
    with open(rubylang_paths[i]) as f:
        contents = f.read()
        #python_programs.append(python_paths[i].split('\\')[-1])
        #python_codes.append(contents)
        ids=list_of_identifiers(contents, ruby_parser)
        #print(contents)
        #print(ids)
        contents=contents.split('\n')
        print('\n')
        print("output1 for", rubylang_paths.split('\\')[-1])
        for node in ids:
            print("identifier-",contents[node.start_point[0]][node.start_point[1]:node.end_point[1]],"at Row no",node.start_point[0],"Col No",node.start_point[1])
    print('-----------------------------------------------------------------------------------')

sys.stdout.close()