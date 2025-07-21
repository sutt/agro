make the command_str/command arg optional and not valid in "agro muster" when the -c flag is passed. For examples:

agro muster -c my_command 'git log' -> invalid command: don't supply a command 

agro muster -c my_command output/my-feat.{1,2} -> valid, run the command associate with my_command on branches my-feat.1 and my-feat.2

agro muster 'git log' output/my-feat -> valid, run git log command on all branches matching output/my-feat*

Add tests to validate this behavior and any other edge cases you can think of.