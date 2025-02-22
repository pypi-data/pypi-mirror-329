from ..commands import command_decorator
from ..hookspec import deltabot_hookimpl


@deltabot_hookimpl
def deltabot_init_parser(parser) -> None:
    parser.add_subcommand(DB)


def slash_scoped_key(key: str) -> tuple:
    i = key.find("/")
    if i == -1:
        raise ValueError("key {!r} does not contain a '/' scope delimiter")
    return (key[:i], key[i + 1 :])


class DB:
    """low level settings."""

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-l", "--list", help="list all key,values.", metavar="SCOPE", nargs="?"
        )
        parser.add_argument(
            "-g",
            "--get",
            help="get a low level setting.",
            metavar="KEY",
            type=slash_scoped_key,
        )
        parser.add_argument(
            "-s",
            "--set",
            help="set a low level setting.",
            metavar=("KEY", "VALUE"),
            nargs=2,
        )
        parser.add_argument(
            "-d",
            "--del",
            help="delete a low level setting.",
            metavar="KEY",
            type=slash_scoped_key,
            dest="_del",
        )

    def run(self, bot, args, out) -> None:
        if args.get:
            self._get(bot, *args.get, out)
        elif args._del:
            self._del(bot, *args._del, out)
        elif args.set:
            self._set(bot, *args.set)
        else:
            self._list(bot, args.list, out)

    def _get(self, bot, scope, key, out) -> None:
        res = bot.get(key, scope=scope)
        if res is None:
            out.fail(f"key {scope}/{key} does not exist")
        else:
            out.line(res)

    def _set(self, bot, key, value) -> None:
        scope, key = slash_scoped_key(key)
        bot.set(key, value, scope=scope)

    def _list(self, bot, scope, out) -> None:
        for key, res in bot.list_settings(scope):
            if "\n" in res:
                out.line(f"{key}:")
                for line in res.split("\n"):
                    out.line("   " + line)
            else:
                out.line(f"{key}: {res}")

    def _del(self, bot, scope, key, out) -> None:
        res = bot.get(key, scope=scope)
        if res is None:
            out.fail(f"key {scope}/{key} does not exist")
        else:
            bot.delete(key, scope=scope)
            out.line(f"key {scope}/{key} deleted")


@command_decorator(name="/set")
def cmd_set(bot, payload, message, replies) -> None:
    """show all available settings or set a value for a setting.

    Examples:

    # show all settings
    /set

    # unset one setting named "mysetting"
    /set_mysetting

    # set one setting named "mysetting"
    /set_mysetting value
    """
    addr = message.get_sender_contact().addr
    if not payload:
        text = dump_settings(bot, scope=addr)
    else:
        args = payload.split(maxsplit=1)
        name = args[0]
        if bot.get_preference_description(name) is None:
            text = "Invalid setting. Available settings:"
            for name, desc in bot.get_preferences():
                text += f"\n\n/set_{name}: {desc}"
        else:
            value = None if len(args) == 1 else args[1]
            old = bot.set(name, value and value.strip(), scope=addr)
            text = f"old: {name}={old!r}\nnew: {name}={value!r}"
    replies.add(text=text)


def dump_settings(bot, scope) -> str:
    lines = []
    for name, desc in bot.get_preferences():
        value = bot.get(name, scope=scope)
        lines.append(f"/set_{name} = {value}\nDescription: {desc}\n")
    if not lines:
        return "no settings"
    return "\n".join(lines)


class TestCommandSettings:
    def test_mock_get_set_empty_settings(self, mocker):
        reply_msg = mocker.get_one_reply("/set")
        assert reply_msg.text.startswith("no settings")

    def test_mock_set_works(self, mocker):
        reply_msg = mocker.get_one_reply("/set hello world")
        assert "old" in reply_msg.text
        msg_reply = mocker.get_one_reply("/set")
        assert msg_reply.text == "hello=world"

    def test_get_set_functional(self, bot_tester):
        msg_reply = bot_tester.send_command("/set hello world")
        msg_reply = bot_tester.send_command("/set hello2 world2")
        msg_reply = bot_tester.send_command("/set")
        assert "hello=world" in msg_reply.text
        assert "hello2=world2" in msg_reply.text
        msg_reply = bot_tester.send_command("/set hello")
        assert "hello=None" in msg_reply.text
