import os
import configparser
from argparse import ArgumentParser
import shlex

from IPython.core.magic import Magics, magics_class, line_cell_magic, line_magic
from IPython import get_ipython
from IPython.display import display, SVG

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

        if args.connection_string is None and args.database_config is None:
            print(
                "Either connection string (-c) or database config (-D) must be provided"
            )
            return

        # Process include/exclude tables
        include_tables = (
            [t.strip() for t in args.include_tables.split(",")]
            if args.include_tables
            else None
        )
        exclude_tables = (
            [t.strip() for t in args.exclude_tables.split(",")]
            if args.exclude_tables
            else None
        )

        # Get connection string
        if args.connection_string is not None:
            connection_string = args.connection_string
        else:
            config = configparser.ConfigParser()
            if "HOME" not in os.environ:
                print("Can't find $HOME environment variable.")
                return

            config_path = os.path.join(os.environ["HOME"], ".jupysql/connections.ini")
            config.read(config_path)

            if not config.sections() or args.database_config not in config.sections():
                print(f"Error: can't find {args.database_config} in {config_path}")
                return

            connection_string = (
                "{drivername}://{username}:{password}@{host}:{port}/{database}".format(
                    **config[args.database_config]
                )
            )

        from .eralchemy_api import generate_er

        if args.mode in ["dot", "er", "mermaid_er"]:
            # For text-based output, use generate_er
            result = generate_er(
                input_source=connection_string,
                mode=args.mode,
                title=args.title,
                include_tables=include_tables,
                exclude_tables=exclude_tables,
            )

            if args.mode=="dot" and (args.embed or args.widget_name):
                if args.widget_name:
                    self._set_widget(args.widget_name)
                elif args.embed:
                    if not self.widget:
                        self.setwidget()
                        self.widget.ready()
                if args.widget_name or args.embed or args.timeout>0:
                    if self.widget is None:
                        print(
                            "Error: No widget / widget name set. Use %set_myAnywidget_object first to set the name."
                        )
                        return
                    elif result:
                        # Get the actual widget
                        w = self.widget
                        w.set_code_content(result)
                        autorespond = bool(args.timeout or args.embed)
                        if autorespond:
                            timeout = args.timeout if args.timeout > 0 else 5
                            w.blocking_reply(timeout)
                            if w.svg:
                                display(SVG(w.svg))
                            else:
                                display(f"No SVG?")

            else:
                return result


# Function to register the magic
def load_ipython_extension(ipython):
    ipython.register_magics(SQLSchemaDisplayMagic)


ip = get_ipython()
ip.register_magics(SQLSchemaDisplayMagic)
