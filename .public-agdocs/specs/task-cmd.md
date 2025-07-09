add the command "agro task" that will generate a md file in the specs directory and open the editor to view the file.
- create .agdocs/specs/<task-name>.md 
- agro task [task-name]
    - if task-name not supplied create a prompt for the user to type one. the task name should not include the md extension, that is implied.
- create a config var AGRO_EDITOR_CMD thats defaults to "code" (for vscode) for the editor opening portion