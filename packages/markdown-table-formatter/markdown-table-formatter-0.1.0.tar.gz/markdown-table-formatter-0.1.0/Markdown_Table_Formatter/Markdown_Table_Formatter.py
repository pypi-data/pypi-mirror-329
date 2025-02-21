import argparse
import re

def format_table(md_table: str) -> str:
    """
    Takes a raw Markdown table and aligns it properly.
    """
    # Split the table into rows
    rows = md_table.strip().split('\n')

    # Split each row by '|' (pipe) to get columns
    table_data = [row.split('|') for row in rows]

    # Clean up leading/trailing spaces from columns
    table_data = [[col.strip() for col in row] for row in table_data]

    # Find the maximum column width for each column
    max_column_widths = [max(len(col) for col in col_group) for col_group in zip(*table_data)]

    # Format each row so that each column is aligned
    formatted_table = []
    for row in table_data:
        formatted_row = " | ".join(f"{col:<{max_column_widths[i]}}" for i, col in enumerate(row))
        formatted_table.append(formatted_row)

    # Join the rows back into a single string
    return "\n".join(formatted_table)

def format_markdown_file(input_file: str, output_file: str):
    """
    Read a markdown file, format the tables, and save it to a new file.
    """
    with open(input_file, 'r') as file:
        content = file.read()

    # Find tables in the markdown file (simple regex to find pipe-based tables)
    table_pattern = re.compile(r'(\|(.+)\|[\r\n]+(?:\|[-\s]+\|[\r\n]+)*)(?=\n|$)')
    tables = table_pattern.findall(content)

    # Format each table and replace it in the content
    for table, _ in tables:
        formatted_table = format_table(table)
        content = content.replace(table, formatted_table)

    # Write the formatted content to a new file
    with open(output_file, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description="Format Markdown tables to align columns.")
    parser.add_argument("input", help="Input Markdown file to format")
    parser.add_argument("output", help="Output file to save formatted Markdown")
    args = parser.parse_args()

    format_markdown_file(args.input, args.output)
    print(f"Formatted Markdown saved to {args.output}")

if __name__ == "__main__":
    main()
