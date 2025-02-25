import pathlib

source_dir = pathlib.Path(__file__).parent.resolve()

XML_FORMAT: str | None = None
with open(f"{source_dir}/answer.xml", "r") as f:
    XML_FORMAT = f.read()
