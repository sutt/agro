add an optional yaml config for agro.
the default place to look to load it is .agdocs/conf/agro.conf.yml
add all the variables from the current expected .env, and change config to load from yaml instead.
also:
create a template config on "agro init" command. the template file will have comments explaining what the config does and a commented to out default version.