# Changelog

## [v4.1.1]

- fix bug in default account detection when there is only one account in ~/.simplebot/accounts

## [v4.1.0]

- allow classic email
- fix bug on registering function command with custom description

## [v4.0.0]

- adapted to deltachat API breaking changes introduced in 1.94.0
- improve detection of group title changes

## [v3.3.0]

- added `hidden` argument to the command and filter declarations hooks, to hide them from the bot's help message

## [v3.2.0]

- added support for importing/exporting backups and keys

## [v3.1.0]

- updated to make use of new deltachat API

## [v3.0.0]

- added support for message processing via webxdc interfaces, requests must have the form: `{payload: {simplebot: {text: "/help"}}}`, only "text" and "html" messages supported for now
- breaking change: message IDs queue table modified to support special incoming webxdc messages
- adapt simplebot's pytest plugin to deltachat's new pytest plugin API

## [v2.4.0]

- fixed to be compatible with `deltachat>=1.66.0`
- commands, filters and plugins are now sorted alphabetically in the help.
- allow to set custom configuration values (ex. custom servers and ports) in `init` subcommand to support servers with not standard configurations.
- added `Dockerfile` to repo to help setting up the bot (thanks @lerdem)

## [v2.3.0]

- close "bytefile" (passed to `Replies.add`) after reading the content.
- use a custom event thread to prevent dead `EventThread`.
- honor `--stdlog` value in log file.
- if filter returns `True`, stop message processing without exceptions.

## [v2.2.1]

- fixed bug while processing member added/removed events from self.

## [v2.2.0]

- show shield badge in commands/filters for bot administrators.
- make commands case insensitive, now `/Help` is equivalent to `/help`.

## [v2.1.1]

- mark messages as read before processing them.

## [v2.1.0]

- mark messages as read so MDN work, if enabled.

## [v2.0.0]

- ignore messages from other bots using the new Delta Chat API. Added `deltabot_incoming_bot_message` hook to process messages from bots.
- allow to get account configuration values with `set_config` command.
- allow to register administrators-only filters.
- send bot's help as HTML message.
- disable "move to DeltaChat folder" (mvbox_move setting) by default.
- log less info if not in "debug" mode.
- help command now also includes filters descriptions.
- **breaking change:** plugins must register their "user preferences" with `DeltaBot.add_preference()` then the setting will be available to users with `/set` command.
- **breaking change:** improved command and filter registration.
- **breaking change:** changed configuration folder to `~/.simplebot`

## [v1.1.1]

- fix bug in `simplebot.utils.get_default_account()` (#72)

## [v1.1.0]

- Improved pytestplugin to allow simulating incoming messages with encryption errors (#68)

## [v1.0.1]

- **From upstream:** major rewrite of deltabot to use new deltachat core python bindings
  which are pluginized themselves.
- Changed SimpleBot logo (thanks Dann) and added default avatar
  generation based on account color.
- Added `@simplebot.command` and `@simplebot.filter` decorators to
  simplify commands and filters creation.
- Added new hooks `deltabot_ban`, `deltabot_unban`,
  `deltabot_title_changed` and `deltabot_image_changed`
- Added options to influence filter execution order.
- Added support for commands that are available only to bot administrators.
- Improved command line, added account manager, administrator tools,
  options to set avatar, display name, status and other low level
  settings for non-standard servers.
- Added default status message.
- Improved code readability with type hints.

## v0.10.0

- initial release

[v4.1.1]: https://github.com/simplebot-org/simplebot/compare/v4.1.0...v4.1.1
[v4.1.0]: https://github.com/simplebot-org/simplebot/compare/v4.0.0...v4.1.0
[v4.0.0]: https://github.com/simplebot-org/simplebot/compare/v3.3.0...v4.0.0
[v3.3.0]: https://github.com/simplebot-org/simplebot/compare/v3.2.0...v3.3.0
[v3.2.0]: https://github.com/simplebot-org/simplebot/compare/v3.1.0...v3.2.0
[v3.1.0]: https://github.com/simplebot-org/simplebot/compare/v3.0.0...v3.1.0
[v3.0.0]: https://github.com/simplebot-org/simplebot/compare/v2.4.0...v3.0.0
[v2.4.0]: https://github.com/simplebot-org/simplebot/compare/v2.3.0...v2.4.0
[v2.3.0]: https://github.com/simplebot-org/simplebot/compare/v2.2.1...v2.3.0
[v2.2.1]: https://github.com/simplebot-org/simplebot/compare/v2.2.0...v2.2.1
[v2.2.0]: https://github.com/simplebot-org/simplebot/compare/v2.1.1...v2.2.0
[v2.1.1]: https://github.com/simplebot-org/simplebot/compare/v2.1.0...v2.1.1
[v2.1.0]: https://github.com/simplebot-org/simplebot/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/simplebot-org/simplebot/compare/v1.1.1...v2.0.0
[v1.1.1]: https://github.com/simplebot-org/simplebot/compare/v1.1.0...v1.1.1
[v1.1.0]: https://github.com/simplebot-org/simplebot/compare/v1.0.1...v1.1.0
[v1.0.1]: https://github.com/simplebot-org/simplebot/compare/v0.10.0...v1.0.1
