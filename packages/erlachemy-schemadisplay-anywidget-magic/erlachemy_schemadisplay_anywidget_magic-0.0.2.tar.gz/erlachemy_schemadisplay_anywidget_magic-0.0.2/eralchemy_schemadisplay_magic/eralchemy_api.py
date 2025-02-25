from typing import Optional, List, Union
from sqlalchemy import MetaData
import logging

logging.disable(logging.CRITICAL)


def generate_er(
    input_source: Union[str, MetaData],
    mode: str = "dot",
    title: Optional[str] = None,
    schema: Optional[str] = None,
    include_tables: Optional[List[str]] = None,
    include_columns: Optional[List[str]] = None,
    exclude_tables: Optional[List[str]] = None,
    exclude_columns: Optional[List[str]] = None,
) -> str:
    """
    Generate an ER diagram and return it as a string.
    Only works for text-based output formats like 'dot' or 'er'.
    For binary formats like PNG, use generate_er_diagram() instead.

    Args:
        input_source (Union[str, MetaData]): Either a database URI string or SQLAlchemy MetaData object
        mode (str, optional): Output mode/format. Must be 'dot' or 'er'. Defaults to "dot".
        title (str, optional): Title for the output graph. Defaults to None.
        schema (str, optional): Database schema name. Defaults to None.
        include_tables (List[str], optional): Tables to include exclusively. Defaults to None.
        include_columns (List[str], optional): Columns to include exclusively. Defaults to None.
        exclude_tables (List[str], optional): Tables to exclude. Defaults to None.
        exclude_columns (List[str], optional): Columns to exclude. Defaults to None.

    Returns:
        str: The generated diagram in the specified format

    Raises:
        ValueError: If mode is not 'dot' or 'er'
    """
    from eralchemy import render_er
    import tempfile

    if mode not in ["dot", "er", "mermaid_er"]:
        raise ValueError(
            "For string output, mode must be 'dot' or 'er'. For other formats, use generate_er_diagram()"
        )

    # Create a temporary file to capture the output
    with tempfile.NamedTemporaryFile(mode="w+", suffix=f".{mode}") as tmp:
        render_er(
            input_source,
            tmp.name,
            mode,
            title=title,
            include_tables=include_tables,
            include_columns=include_columns,
            exclude_tables=exclude_tables,
            exclude_columns=exclude_columns,
            schema=schema,
        )
        tmp.seek(0)
        return tmp.read()
