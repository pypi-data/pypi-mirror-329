# erlachemy_schemadisplay_anywidget_magic

IPython magic to generate a database schema using `eralchemy` and display it using `jupyter_anywidget_graphviz` Graphviz WASM anywidget.

Install from PyPi as:

`pip install erlachemy_schemadisplay_anywidget_magic`

Enable magics: `%load_ext eralchemy_schemadisplay_magic`

Create magic with "hidden" graphviz anywidget: `%schema_magic_init`

Alternatively, create an anywidget and pass it it:

```python

from jupyter_anywidget_graphviz import (
    graphviz_headless,
)

g = graphviz_headless()
%schema_magic_init g
```

Create example database:

```python

import sqlite3


def create_database():
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    # Create the parent table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """
    )

    # Create the child table with a foreign key reference to users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """
    )

    # Commit and close
    conn.commit()
    conn.close()

create_database()
```

Generate schema as dot script and render using graphviz widget:

__Note that this requires the `-m / --mode` to be set to `dot`, which it is by default, although we can also pass it explicitly.

```python
dot_data = %schema_magic -c "sqlite:///example.db" -m dot

from IPython.display import SVG
SVG( g.render(dot_data)["svg"] )
```

If we pass a widget in to the magic, and we have a "full" `anywidget` running environment (not JupyterLite/pyodide), we can use the `-e / --embed` switch to return the dot diagram rendered as SVG (this will attempt to create/use an internally created graphviz widget). Alternatively, we can pass a grpahviz widget using the `-w / --widget-name` parameter.

`%schema_magic -c "sqlite:///example.db" -m dot -e`

`%schema_magic -c "sqlite:///example.db" -m dot -w g`


![Example of generating schema diagrma using magic](images/example.png)


TO DO - fix things so it works in Marimo:

- remove IPython refs
- move function to create and render dot file out of magic and into a cleaner py api