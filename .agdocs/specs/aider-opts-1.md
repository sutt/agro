Below I'll include a printout of the aider's cli help.

I want to pass some arguments to this script via arguments on the maider.sh shell out.

The goals I want are:
1. don't prompt user for any updates in the aider package
2. don't leave attribution to aider anywhere in the git author or commit message. (this could be multiple flags?)

usage: aider [-h] [--model MODEL] [--openai-api-key OPENAI_API_KEY]
             [--anthropic-api-key ANTHROPIC_API_KEY]
             [--openai-api-base OPENAI_API_BASE]
             [--openai-api-type OPENAI_API_TYPE]
             [--openai-api-version OPENAI_API_VERSION]
             [--openai-api-deployment-id OPENAI_API_DEPLOYMENT_ID]
             [--openai-organization-id OPENAI_ORGANIZATION_ID]
             [--set-env ENV_VAR_NAME=value] [--api-key PROVIDER=KEY]
             [--list-models MODEL] [--model-settings-file MODEL_SETTINGS_FILE]
             [--model-metadata-file MODEL_METADATA_FILE] [--alias ALIAS:MODEL]
             [--reasoning-effort REASONING_EFFORT]
             [--thinking-tokens THINKING_TOKENS]
             [--verify-ssl | --no-verify-ssl] [--timeout TIMEOUT]
             [--edit-format EDIT_FORMAT] [--architect]
             [--auto-accept-architect | --no-auto-accept-architect]
             [--weak-model WEAK_MODEL] [--editor-model EDITOR_MODEL]
             [--editor-edit-format EDITOR_EDIT_FORMAT]
             [--show-model-warnings | --no-show-model-warnings]
             [--check-model-accepts-settings | --no-check-model-accepts-settings]
             [--max-chat-history-tokens MAX_CHAT_HISTORY_TOKENS]
             [--cache-prompts | --no-cache-prompts]
             [--cache-keepalive-pings CACHE_KEEPALIVE_PINGS]
             [--map-tokens MAP_TOKENS]
             [--map-refresh {auto,always,files,manual}]
             [--map-multiplier-no-files MAP_MULTIPLIER_NO_FILES]
             [--input-history-file INPUT_HISTORY_FILE]
             [--chat-history-file CHAT_HISTORY_FILE]
             [--restore-chat-history | --no-restore-chat-history]
             [--llm-history-file LLM_HISTORY_FILE] [--dark-mode]
             [--light-mode] [--pretty | --no-pretty] [--stream | --no-stream]
             [--user-input-color USER_INPUT_COLOR]
             [--tool-output-color TOOL_OUTPUT_COLOR]
             [--tool-error-color TOOL_ERROR_COLOR]
             [--tool-warning-color TOOL_WARNING_COLOR]
             [--assistant-output-color ASSISTANT_OUTPUT_COLOR]
             [--completion-menu-color COLOR]
             [--completion-menu-bg-color COLOR]
             [--completion-menu-current-color COLOR]
             [--completion-menu-current-bg-color COLOR]
             [--code-theme CODE_THEME] [--show-diffs] [--git | --no-git]
             [--gitignore | --no-gitignore]
             [--add-gitignore-files | --no-add-gitignore-files]
             [--aiderignore AIDERIGNORE] [--subtree-only]
             [--auto-commits | --no-auto-commits]
             [--dirty-commits | --no-dirty-commits]
             [--attribute-author | --no-attribute-author]
             [--attribute-committer | --no-attribute-committer]
             [--attribute-commit-message-author | --no-attribute-commit-message-author]
             [--attribute-commit-message-committer | --no-attribute-commit-message-committer]
             [--attribute-co-authored-by | --no-attribute-co-authored-by]
             [--git-commit-verify | --no-git-commit-verify] [--commit]
             [--commit-prompt PROMPT] [--dry-run | --no-dry-run]
             [--skip-sanity-check-repo] [--watch-files | --no-watch-files]
             [--lint] [--lint-cmd LINT_CMD] [--auto-lint | --no-auto-lint]
             [--test-cmd TEST_CMD] [--auto-test | --no-auto-test] [--test]
             [--analytics | --no-analytics]
             [--analytics-log ANALYTICS_LOG_FILE] [--analytics-disable]
             [--analytics-posthog-host ANALYTICS_POSTHOG_HOST]
             [--analytics-posthog-project-api-key ANALYTICS_POSTHOG_PROJECT_API_KEY]
             [--just-check-update] [--check-update | --no-check-update]
             [--show-release-notes | --no-show-release-notes]
             [--install-main-branch] [--upgrade] [--version]
             [--message COMMAND] [--message-file MESSAGE_FILE]
             [--gui | --no-gui | --browser | --no-browser]
             [--copy-paste | --no-copy-paste] [--apply FILE]
             [--apply-clipboard-edits] [--exit] [--show-repo-map]
             [--show-prompts] [--voice-format VOICE_FORMAT]
             [--voice-language VOICE_LANGUAGE]
             [--voice-input-device VOICE_INPUT_DEVICE] [--disable-playwright]
             [--file FILE] [--read FILE] [--vim]
             [--chat-language CHAT_LANGUAGE]
             [--commit-language COMMIT_LANGUAGE] [--yes-always] [-v]
             [--load LOAD_FILE] [--encoding ENCODING]
             [--line-endings {platform,lf,crlf}] [-c CONFIG_FILE]
             [--env-file ENV_FILE]
             [--suggest-shell-commands | --no-suggest-shell-commands]
             [--fancy-input | --no-fancy-input] [--multiline | --no-multiline]
             [--notifications | --no-notifications]
             [--notifications-command COMMAND]
             [--detect-urls | --no-detect-urls] [--editor EDITOR]
             [--shell-completions SHELL] [--opus] [--sonnet] [--haiku] [--4]
             [--4o] [--mini] [--4-turbo] [--35turbo] [--deepseek] [--o1-mini]
             [--o1-preview]
             [FILE ...]

aider is AI pair programming in your terminal

options:
  -h, --help            show this help message and exit

Main model:
  FILE                  files to edit with an LLM (optional)
  --model MODEL         Specify the model to use for the main chat [env var:
                        AIDER_MODEL]

API Keys and settings:
  --openai-api-key OPENAI_API_KEY
                        Specify the OpenAI API key [env var:
                        AIDER_OPENAI_API_KEY]
  --anthropic-api-key ANTHROPIC_API_KEY
                        Specify the Anthropic API key [env var:
                        AIDER_ANTHROPIC_API_KEY]
  --openai-api-base OPENAI_API_BASE
                        Specify the api base url [env var:
                        AIDER_OPENAI_API_BASE]
  --openai-api-type OPENAI_API_TYPE
                        (deprecated, use --set-env OPENAI_API_TYPE=<value>)
                        [env var: AIDER_OPENAI_API_TYPE]
  --openai-api-version OPENAI_API_VERSION
                        (deprecated, use --set-env OPENAI_API_VERSION=<value>)
                        [env var: AIDER_OPENAI_API_VERSION]
  --openai-api-deployment-id OPENAI_API_DEPLOYMENT_ID
                        (deprecated, use --set-env
                        OPENAI_API_DEPLOYMENT_ID=<value>) [env var:
                        AIDER_OPENAI_API_DEPLOYMENT_ID]
  --openai-organization-id OPENAI_ORGANIZATION_ID
                        (deprecated, use --set-env
                        OPENAI_ORGANIZATION=<value>) [env var:
                        AIDER_OPENAI_ORGANIZATION_ID]
  --set-env ENV_VAR_NAME=value
                        Set an environment variable (to control API settings,
                        can be used multiple times) [env var: AIDER_SET_ENV]
  --api-key PROVIDER=KEY
                        Set an API key for a provider (eg: --api-key
                        provider=<key> sets PROVIDER_API_KEY=<key>) [env var:
                        AIDER_API_KEY]

Model settings:
  --list-models MODEL, --models MODEL
                        List known models which match the (partial) MODEL name
                        [env var: AIDER_LIST_MODELS]
  --model-settings-file MODEL_SETTINGS_FILE
                        Specify a file with aider model settings for unknown
                        models [env var: AIDER_MODEL_SETTINGS_FILE]
  --model-metadata-file MODEL_METADATA_FILE
                        Specify a file with context window and costs for
                        unknown models [env var: AIDER_MODEL_METADATA_FILE]
  --alias ALIAS:MODEL   Add a model alias (can be used multiple times) [env
                        var: AIDER_ALIAS]
  --reasoning-effort REASONING_EFFORT
                        Set the reasoning_effort API parameter (default: not
                        set) [env var: AIDER_REASONING_EFFORT]
  --thinking-tokens THINKING_TOKENS
                        Set the thinking token budget for models that support
                        it. Use 0 to disable. (default: not set) [env var:
                        AIDER_THINKING_TOKENS]
  --verify-ssl, --no-verify-ssl
                        Verify the SSL cert when connecting to models
                        (default: True) [env var: AIDER_VERIFY_SSL]
  --timeout TIMEOUT     Timeout in seconds for API calls (default: None) [env
                        var: AIDER_TIMEOUT]
  --edit-format EDIT_FORMAT, --chat-mode EDIT_FORMAT
                        Specify what edit format the LLM should use (default
                        depends on model) [env var: AIDER_EDIT_FORMAT]
  --architect           Use architect edit format for the main chat [env var:
                        AIDER_ARCHITECT]
  --auto-accept-architect, --no-auto-accept-architect
                        Enable/disable automatic acceptance of architect
                        changes (default: True) [env var:
                        AIDER_AUTO_ACCEPT_ARCHITECT]
  --weak-model WEAK_MODEL
                        Specify the model to use for commit messages and chat
                        history summarization (default depends on --model)
                        [env var: AIDER_WEAK_MODEL]
  --editor-model EDITOR_MODEL
                        Specify the model to use for editor tasks (default
                        depends on --model) [env var: AIDER_EDITOR_MODEL]
  --editor-edit-format EDITOR_EDIT_FORMAT
                        Specify the edit format for the editor model (default:
                        depends on editor model) [env var:
                        AIDER_EDITOR_EDIT_FORMAT]
  --show-model-warnings, --no-show-model-warnings
                        Only work with models that have meta-data available
                        (default: True) [env var: AIDER_SHOW_MODEL_WARNINGS]
  --check-model-accepts-settings, --no-check-model-accepts-settings
                        Check if model accepts settings like
                        reasoning_effort/thinking_tokens (default: True) [env
                        var: AIDER_CHECK_MODEL_ACCEPTS_SETTINGS]
  --max-chat-history-tokens MAX_CHAT_HISTORY_TOKENS
                        Soft limit on tokens for chat history, after which
                        summarization begins. If unspecified, defaults to the
                        model's max_chat_history_tokens. [env var:
                        AIDER_MAX_CHAT_HISTORY_TOKENS]

Cache settings:
  --cache-prompts, --no-cache-prompts
                        Enable caching of prompts (default: False) [env var:
                        AIDER_CACHE_PROMPTS]
  --cache-keepalive-pings CACHE_KEEPALIVE_PINGS
                        Number of times to ping at 5min intervals to keep
                        prompt cache warm (default: 0) [env var:
                        AIDER_CACHE_KEEPALIVE_PINGS]

Repomap settings:
  --map-tokens MAP_TOKENS
                        Suggested number of tokens to use for repo map, use 0
                        to disable [env var: AIDER_MAP_TOKENS]
  --map-refresh {auto,always,files,manual}
                        Control how often the repo map is refreshed. Options:
                        auto, always, files, manual (default: auto) [env var:
                        AIDER_MAP_REFRESH]
  --map-multiplier-no-files MAP_MULTIPLIER_NO_FILES
                        Multiplier for map tokens when no files are specified
                        (default: 2) [env var: AIDER_MAP_MULTIPLIER_NO_FILES]

History Files:
  --input-history-file INPUT_HISTORY_FILE
                        Specify the chat input history file (default:
                        /home/user/tools_dev/agscript/.aider.input.history)
                        [env var: AIDER_INPUT_HISTORY_FILE]
  --chat-history-file CHAT_HISTORY_FILE
                        Specify the chat history file (default:
                        /home/user/tools_dev/agscript/.aider.chat.history.md)
                        [env var: AIDER_CHAT_HISTORY_FILE]
  --restore-chat-history, --no-restore-chat-history
                        Restore the previous chat history messages (default:
                        False) [env var: AIDER_RESTORE_CHAT_HISTORY]
  --llm-history-file LLM_HISTORY_FILE
                        Log the conversation with the LLM to this file (for
                        example, .aider.llm.history) [env var:
                        AIDER_LLM_HISTORY_FILE]

Output settings:
  --dark-mode           Use colors suitable for a dark terminal background
                        (default: False) [env var: AIDER_DARK_MODE]
  --light-mode          Use colors suitable for a light terminal background
                        (default: False) [env var: AIDER_LIGHT_MODE]
  --pretty, --no-pretty
                        Enable/disable pretty, colorized output (default:
                        True) [env var: AIDER_PRETTY]
  --stream, --no-stream
                        Enable/disable streaming responses (default: True)
                        [env var: AIDER_STREAM]
  --user-input-color USER_INPUT_COLOR
                        Set the color for user input (default: #00cc00) [env
                        var: AIDER_USER_INPUT_COLOR]
  --tool-output-color TOOL_OUTPUT_COLOR
                        Set the color for tool output (default: None) [env
                        var: AIDER_TOOL_OUTPUT_COLOR]
  --tool-error-color TOOL_ERROR_COLOR
                        Set the color for tool error messages (default:
                        #FF2222) [env var: AIDER_TOOL_ERROR_COLOR]
  --tool-warning-color TOOL_WARNING_COLOR
                        Set the color for tool warning messages (default:
                        #FFA500) [env var: AIDER_TOOL_WARNING_COLOR]
  --assistant-output-color ASSISTANT_OUTPUT_COLOR
                        Set the color for assistant output (default: #0088ff)
                        [env var: AIDER_ASSISTANT_OUTPUT_COLOR]
  --completion-menu-color COLOR
                        Set the color for the completion menu (default:
                        terminal's default text color) [env var:
                        AIDER_COMPLETION_MENU_COLOR]
  --completion-menu-bg-color COLOR
                        Set the background color for the completion menu
                        (default: terminal's default background color) [env
                        var: AIDER_COMPLETION_MENU_BG_COLOR]
  --completion-menu-current-color COLOR
                        Set the color for the current item in the completion
                        menu (default: terminal's default background color)
                        [env var: AIDER_COMPLETION_MENU_CURRENT_COLOR]
  --completion-menu-current-bg-color COLOR
                        Set the background color for the current item in the
                        completion menu (default: terminal's default text
                        color) [env var:
                        AIDER_COMPLETION_MENU_CURRENT_BG_COLOR]
  --code-theme CODE_THEME
                        Set the markdown code theme (default: default, other
                        options include monokai, solarized-dark, solarized-
                        light, or a Pygments builtin style, see
                        https://pygments.org/styles for available themes) [env
                        var: AIDER_CODE_THEME]
  --show-diffs          Show diffs when committing changes (default: False)
                        [env var: AIDER_SHOW_DIFFS]

Git settings:
  --git, --no-git       Enable/disable looking for a git repo (default: True)
                        [env var: AIDER_GIT]
  --gitignore, --no-gitignore
                        Enable/disable adding .aider* to .gitignore (default:
                        True) [env var: AIDER_GITIGNORE]
  --add-gitignore-files, --no-add-gitignore-files
                        Enable/disable the addition of files listed in
                        .gitignore to Aider's editing scope. [env var:
                        AIDER_ADD_GITIGNORE_FILES]
  --aiderignore AIDERIGNORE
                        Specify the aider ignore file (default: .aiderignore
                        in git root) [env var: AIDER_AIDERIGNORE]
  --subtree-only        Only consider files in the current subtree of the git
                        repository [env var: AIDER_SUBTREE_ONLY]
  --auto-commits, --no-auto-commits
                        Enable/disable auto commit of LLM changes (default:
                        True) [env var: AIDER_AUTO_COMMITS]
  --dirty-commits, --no-dirty-commits
                        Enable/disable commits when repo is found dirty
                        (default: True) [env var: AIDER_DIRTY_COMMITS]
  --attribute-author, --no-attribute-author
                        Attribute aider code changes in the git author name
                        (default: True). If explicitly set to True, overrides
                        --attribute-co-authored-by precedence. [env var:
                        AIDER_ATTRIBUTE_AUTHOR]
  --attribute-committer, --no-attribute-committer
                        Attribute aider commits in the git committer name
                        (default: True). If explicitly set to True, overrides
                        --attribute-co-authored-by precedence for aider edits.
                        [env var: AIDER_ATTRIBUTE_COMMITTER]
  --attribute-commit-message-author, --no-attribute-commit-message-author
                        Prefix commit messages with 'aider: ' if aider
                        authored the changes (default: False) [env var:
                        AIDER_ATTRIBUTE_COMMIT_MESSAGE_AUTHOR]
  --attribute-commit-message-committer, --no-attribute-commit-message-committer
                        Prefix all commit messages with 'aider: ' (default:
                        False) [env var:
                        AIDER_ATTRIBUTE_COMMIT_MESSAGE_COMMITTER]
  --attribute-co-authored-by, --no-attribute-co-authored-by
                        Attribute aider edits using the Co-authored-by trailer
                        in the commit message (default: True). If True, this
                        takes precedence over default --attribute-author and
                        --attribute-committer behavior unless they are
                        explicitly set to True. [env var:
                        AIDER_ATTRIBUTE_CO_AUTHORED_BY]
  --git-commit-verify, --no-git-commit-verify
                        Enable/disable git pre-commit hooks with --no-verify
                        (default: False) [env var: AIDER_GIT_COMMIT_VERIFY]
  --commit              Commit all pending changes with a suitable commit
                        message, then exit [env var: AIDER_COMMIT]
  --commit-prompt PROMPT
                        Specify a custom prompt for generating commit messages
                        [env var: AIDER_COMMIT_PROMPT]
  --dry-run, --no-dry-run
                        Perform a dry run without modifying files (default:
                        False) [env var: AIDER_DRY_RUN]
  --skip-sanity-check-repo
                        Skip the sanity check for the git repository (default:
                        False) [env var: AIDER_SKIP_SANITY_CHECK_REPO]
  --watch-files, --no-watch-files
                        Enable/disable watching files for ai coding comments
                        (default: False) [env var: AIDER_WATCH_FILES]

Fixing and committing:
  --lint                Lint and fix provided files, or dirty files if none
                        provided [env var: AIDER_LINT]
  --lint-cmd LINT_CMD   Specify lint commands to run for different languages,
                        eg: "python: flake8 --select=..." (can be used
                        multiple times) [env var: AIDER_LINT_CMD]
  --auto-lint, --no-auto-lint
                        Enable/disable automatic linting after changes
                        (default: True) [env var: AIDER_AUTO_LINT]
  --test-cmd TEST_CMD   Specify command to run tests [env var: AIDER_TEST_CMD]
  --auto-test, --no-auto-test
                        Enable/disable automatic testing after changes
                        (default: False) [env var: AIDER_AUTO_TEST]
  --test                Run tests, fix problems found and then exit [env var:
                        AIDER_TEST]

Analytics:
  --analytics, --no-analytics
                        Enable/disable analytics for current session (default:
                        random) [env var: AIDER_ANALYTICS]
  --analytics-log ANALYTICS_LOG_FILE
                        Specify a file to log analytics events [env var:
                        AIDER_ANALYTICS_LOG]
  --analytics-disable   Permanently disable analytics [env var:
                        AIDER_ANALYTICS_DISABLE]
  --analytics-posthog-host ANALYTICS_POSTHOG_HOST
                        Send analytics to custom PostHog instance [env var:
                        AIDER_ANALYTICS_POSTHOG_HOST]
  --analytics-posthog-project-api-key ANALYTICS_POSTHOG_PROJECT_API_KEY
                        Send analytics to custom PostHog project [env var:
                        AIDER_ANALYTICS_POSTHOG_PROJECT_API_KEY]

Upgrading:
  --just-check-update   Check for updates and return status in the exit code
                        [env var: AIDER_JUST_CHECK_UPDATE]
  --check-update, --no-check-update
                        Check for new aider versions on launch [env var:
                        AIDER_CHECK_UPDATE]
  --show-release-notes, --no-show-release-notes
                        Show release notes on first run of new version
                        (default: None, ask user) [env var:
                        AIDER_SHOW_RELEASE_NOTES]
  --install-main-branch
                        Install the latest version from the main branch [env
                        var: AIDER_INSTALL_MAIN_BRANCH]
  --upgrade, --update   Upgrade aider to the latest version from PyPI [env
                        var: AIDER_UPGRADE]
  --version             Show the version number and exit

Modes:
  --message COMMAND, --msg COMMAND, -m COMMAND
                        Specify a single message to send the LLM, process
                        reply then exit (disables chat mode) [env var:
                        AIDER_MESSAGE]
  --message-file MESSAGE_FILE, -f MESSAGE_FILE
                        Specify a file containing the message to send the LLM,
                        process reply, then exit (disables chat mode) [env
                        var: AIDER_MESSAGE_FILE]
  --gui, --no-gui, --browser, --no-browser
                        Run aider in your browser (default: False) [env var:
                        AIDER_GUI]
  --copy-paste, --no-copy-paste
                        Enable automatic copy/paste of chat between aider and
                        web UI (default: False) [env var: AIDER_COPY_PASTE]
  --apply FILE          Apply the changes from the given file instead of
                        running the chat (debug) [env var: AIDER_APPLY]
  --apply-clipboard-edits
                        Apply clipboard contents as edits using the main
                        model's editor format [env var:
                        AIDER_APPLY_CLIPBOARD_EDITS]
  --exit                Do all startup activities then exit before accepting
                        user input (debug) [env var: AIDER_EXIT]
  --show-repo-map       Print the repo map and exit (debug) [env var:
                        AIDER_SHOW_REPO_MAP]
  --show-prompts        Print the system prompts and exit (debug) [env var:
                        AIDER_SHOW_PROMPTS]

Voice settings:
  --voice-format VOICE_FORMAT
                        Audio format for voice recording (default: wav). webm
                        and mp3 require ffmpeg [env var: AIDER_VOICE_FORMAT]
  --voice-language VOICE_LANGUAGE
                        Specify the language for voice using ISO 639-1 code
                        (default: auto) [env var: AIDER_VOICE_LANGUAGE]
  --voice-input-device VOICE_INPUT_DEVICE
                        Specify the input device name for voice recording [env
                        var: AIDER_VOICE_INPUT_DEVICE]

Other settings:
  --disable-playwright  Never prompt for or attempt to install Playwright for
                        web scraping (default: False). [env var:
                        AIDER_DISABLE_PLAYWRIGHT]
  --file FILE           specify a file to edit (can be used multiple times)
                        [env var: AIDER_FILE]
  --read FILE           specify a read-only file (can be used multiple times)
                        [env var: AIDER_READ]
  --vim                 Use VI editing mode in the terminal (default: False)
                        [env var: AIDER_VIM]
  --chat-language CHAT_LANGUAGE
                        Specify the language to use in the chat (default:
                        None, uses system settings) [env var:
                        AIDER_CHAT_LANGUAGE]
  --commit-language COMMIT_LANGUAGE
                        Specify the language to use in the commit message
                        (default: None, user language) [env var:
                        AIDER_COMMIT_LANGUAGE]
  --yes-always          Always say yes to every confirmation [env var:
                        AIDER_YES_ALWAYS]
  -v, --verbose         Enable verbose output [env var: AIDER_VERBOSE]
  --load LOAD_FILE      Load and execute /commands from a file on launch [env
                        var: AIDER_LOAD]
  --encoding ENCODING   Specify the encoding for input and output (default:
                        utf-8) [env var: AIDER_ENCODING]
  --line-endings {platform,lf,crlf}
                        Line endings to use when writing files (default:
                        platform) [env var: AIDER_LINE_ENDINGS]
  -c CONFIG_FILE, --config CONFIG_FILE
                        Specify the config file (default: search for
                        .aider.conf.yml in git root, cwd or home directory)
  --env-file ENV_FILE   Specify the .env file to load (default: .env in git
                        root) [env var: AIDER_ENV_FILE]
  --suggest-shell-commands, --no-suggest-shell-commands
                        Enable/disable suggesting shell commands (default:
                        True) [env var: AIDER_SUGGEST_SHELL_COMMANDS]
  --fancy-input, --no-fancy-input
                        Enable/disable fancy input with history and completion
                        (default: True) [env var: AIDER_FANCY_INPUT]
  --multiline, --no-multiline
                        Enable/disable multi-line input mode with Meta-Enter
                        to submit (default: False) [env var: AIDER_MULTILINE]
  --notifications, --no-notifications
                        Enable/disable terminal bell notifications when LLM
                        responses are ready (default: False) [env var:
                        AIDER_NOTIFICATIONS]
  --notifications-command COMMAND
                        Specify a command to run for notifications instead of
                        the terminal bell. If not specified, a default command
                        for your OS may be used. [env var:
                        AIDER_NOTIFICATIONS_COMMAND]
  --detect-urls, --no-detect-urls
                        Enable/disable detection and offering to add URLs to
                        chat (default: True) [env var: AIDER_DETECT_URLS]
  --editor EDITOR       Specify which editor to use for the /editor command
                        [env var: AIDER_EDITOR]
  --shell-completions SHELL
                        Print shell completion script for the specified SHELL
                        and exit. Supported shells: bash, tcsh, zsh. Example:
                        aider --shell-completions bash [env var:
                        AIDER_SHELL_COMPLETIONS]

Deprecated model settings:
  --opus                Use claude-3-opus-20240229 model for the main chat
                        (deprecated, use --model) [env var: AIDER_OPUS]
  --sonnet              Use anthropic/claude-3-7-sonnet-20250219 model for the
                        main chat (deprecated, use --model) [env var:
                        AIDER_SONNET]
  --haiku               Use claude-3-5-haiku-20241022 model for the main chat
                        (deprecated, use --model) [env var: AIDER_HAIKU]
  --4, -4               Use gpt-4-0613 model for the main chat (deprecated,
                        use --model) [env var: AIDER_4]
  --4o                  Use gpt-4o model for the main chat (deprecated, use
                        --model) [env var: AIDER_4O]
  --mini                Use gpt-4o-mini model for the main chat (deprecated,
                        use --model) [env var: AIDER_MINI]
  --4-turbo             Use gpt-4-1106-preview model for the main chat
                        (deprecated, use --model) [env var: AIDER_4_TURBO]
  --35turbo, --35-turbo, --3, -3
                        Use gpt-3.5-turbo model for the main chat (deprecated,
                        use --model) [env var: AIDER_35TURBO]
  --deepseek            Use deepseek/deepseek-chat model for the main chat
                        (deprecated, use --model) [env var: AIDER_DEEPSEEK]
  --o1-mini             Use o1-mini model for the main chat (deprecated, use
                        --model) [env var: AIDER_O1_MINI]
  --o1-preview          Use o1-preview model for the main chat (deprecated,
                        use --model) [env var: AIDER_O1_PREVIEW]

Args that start with '--' can also be set in a config file
(/home/user/tools_dev/agscript/.aider.conf.yml or /home/user/.aider.conf.yml
or specified via -c). The config file uses YAML syntax and must represent a
YAML 'mapping' (for details, see http://learn.getgrav.org/advanced/yaml). In
general, command-line values override environment variables which override
config file values which override defaults.

### task
Again modify this script to add the nec args to maider.sh to pass to aider that accomplish:

The goals I want are:
1. don't prompt user for any updates in the aider package
2. don't leave attribution to aider anywhere in the git author or commit message. (this could be multiple flags?)

Don't worry about modifying maider.sh just pass arguments to it which it will pass to aider.