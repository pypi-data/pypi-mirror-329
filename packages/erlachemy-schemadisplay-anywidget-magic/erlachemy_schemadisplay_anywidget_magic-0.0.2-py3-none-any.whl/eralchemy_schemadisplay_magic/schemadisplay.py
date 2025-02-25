import os
import configparser
from argparse import ArgumentParser
import shlex

from IPython.core.magic import Magics, magics_class, line_cell_magic, line_magic
# from IPython import get_ipython
from IPython.display import display, SVG
from .eralchemy_api import generate_er

@magics_class
class SQLSchemaDisplayMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(SQLSchemaDisplayMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data
        self.widget = None

    def _set_widget(self, w_name=""):
        w_name = w_name.strip()
        if w_name:
            self.widget_name = w_name
        self.widget = self.shell.user_ns[self.widget_name]
        # Perhaps add a test that it is a widget type, else None?
        # print(f"graphviz_magic object set to: {self.widget_name}")

    @line_magic
    def schema_magic_init(self, line=""):
        """Set the object name to be used in subsequent myAnywidget_magic calls."""
        if line:
            self._set_widget(line)
        else:
            from jupyter_anywidget_graphviz import (
                graphviz_headless
            )
            self.widget = graphviz_headless()
        # We really need a self.widget.reset() that does things properly
        self.widget.svg = ""
        self.widget.code_content = ""
        self.widget.response = {"status": "ready"}

    @line_magic
    def schema_magic_status(self, line=""):
        """Get the schema magic widget status."""
        if line:
            self._set_widget(line)
        if self.widget:
            print(self.widget.response)
        else:
            print("I think you need to run %schema_magic_init")

    @line_cell_magic
    def schema_magic(self, line, cell=""):
        """
        Magic command to display database schema as an ERD.

        Usage:
            %schema -c "postgresql://user:pass@localhost/dbname"
            %schema -D database_config_name
        """
        parser = ArgumentParser()
        parser.add_argument("-D", "--database_config", default=None)
        parser.add_argument("-c", "--connection_string", default=None)
        parser.add_argument("-t", "--include_tables", default=None)
        parser.add_argument("-x", "--exclude_tables", default=None)
        parser.add_argument("-m", "--mode", default="dot")
        parser.add_argument("-w", "--widget-name", default=None)
        parser.add_argument("-T", "--timeout", default=-1)
        parser.add_argument(
            "-e", "--embed", action="store_true", help="Enable embedding"
        )
        parser.add_argument("--title", default=None)
        # Graphviz components

        args = parser.parse_args(shlex.split(line))

        connection_string = get_attr_or_key(args, "connection_string")
        database_config = get_attr_or_key(args, "database_config")
        mode = get_attr_or_key(args, "mode")
        embed = get_attr_or_key(args, "embed")
        title = get_attr_or_key(args, "title")
        timeout = get_attr_or_key(args, "timeout", -1)
        widget_name = get_attr_or_key(args, "widget_name")
        include_tables = get_attr_or_key(args, "include_tables")
        include_tables = (
            [t.strip() for t in include_tables.split(",")]
            if include_tables
            else None
        )
        exclude_tables = get_attr_or_key(args, "include_tables")
        exclude_tables = (
            [t.strip() for t in include_tables.split(",")]
            if include_tables
            else None
        )
        widget = None
        if mode=="dot" and (embed or widget_name):
            if widget_name:
                self._set_widget(widget_name)
            elif embed:
                if not self.widget:
                    self.setwidget()
                    self.widget.ready()
            widget = self.widget if widget_name or embed or timeout>0 else None
        return render_er_from_db(
            connection_string,
            widget,
            database_config,
            mode,
            title,
            include_tables,
            exclude_tables,
            args,
        )


def render_er_from_db(
    connection_string=None,
    widget=None,
    database_config=None,
    mode="dot",
    title=None,
    include_tables=None,
    exclude_tables=None,
    args=None,
):
    if not connection_string and database_config is None:
        print(
            "Either connection string (-c) or database config (-D) must be provided"
        )
        return

    # Get connection string
    if not connection_string:
        config = configparser.ConfigParser()
        if "HOME" not in os.environ:
            print("Can't find $HOME environment variable.")
            return

        config_path = os.path.join(os.environ["HOME"], ".jupysql/connections.ini")
        config.read(config_path)

        if not config.sections() or database_config not in config.sections():
            print(f"Error: can't find {database_config} in {config_path}")
            return

        connection_string = (
            "{drivername}://{username}:{password}@{host}:{port}/{database}".format(
                **config[database_config]
            )
        )

    if mode in ["dot", "er", "mermaid_er"]:
        result = generate_er(
            input_source=connection_string,
            mode=mode,
            title=title,
            include_tables=include_tables,
            exclude_tables=exclude_tables,
        )

        if widget:
            schema_render_dot(widget, result, args)
        else:
            return result


def get_attr_or_key(obj, name, default=None):
    """Get an attribute from an object or a key from a dictionary.

    Args:
        obj: The object or dictionary.
        name: The attribute name or dictionary key.
        default: The default value if the attribute or key is not found.

    Returns:
        The value of the attribute or key, or the default value.
    """
    if not obj:
        return None
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def schema_render_dot(w, dot, args=None):
    if w is None:
        print(
            "Error: No widget / widget name set. Use %set_myAnywidget_object first to set the name."
        )
        return
    elif dot:
        if args:
            w.set_code_content(dot)
            timeout = get_attr_or_key(args, "timeout", 0)
            timeout = timeout if timeout > 0 else 5
            w.blocking_reply(timeout)
            embed = get_attr_or_key(args, "embed", False)
            autorespond = bool(timeout or embed)
        else:
            autorespond = True
        if autorespond:
            if w.svg:
                display(SVG(w.svg))
            else:
                display(f"No SVG?")


# Function to register the magic
def load_ipython_extension(ipython):
    ipython.register_magics(SQLSchemaDisplayMagic)


# ip = get_ipython()
# ip.register_magics(SQLSchemaDisplayMagic)
