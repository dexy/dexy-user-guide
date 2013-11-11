from inspect import cleandoc as trim
from utils import wrap
import dexy.load_plugins
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

def virtual_file_contents__test():
    with wrap() as wrapper:
        with open("dexy.yaml", 'w') as f:
            f.write(trim("""\
            hello.txt|jinja:
                - contents: "1 + 1 = {{ 1+1 }}"
            """))

        wrapper.run_from_new()
        doc = wrapper.nodes['doc:hello.txt|jinja']
        assert str(doc.output_data()) == "1 + 1 = 2"

def write_text_files():
    os.makedirs("bar/baz")

    with open("foo.txt", 'w') as f:
        f.write("")

    with open("bar.txt", 'w') as f:
        f.write("")

    with open("bar/foo.txt", 'w') as f:
        f.write("")

    with open("bar/baz/foo.txt", 'w') as f:
        f.write("")


def config_txt_ext__test():
    with wrap() as wrapper:
        write_text_files()
        with open("dexy.yaml", 'w') as f:
            f.write(".txt")
        wrapper.run_from_new()

        assert sorted(wrapper.nodes) == [
                'doc:bar.txt',
                'doc:bar/baz/foo.txt',
                'doc:bar/foo.txt',
                'doc:foo.txt',
                'pattern:*.txt'
                ]

def config_txt_single_file__test():
    with wrap() as wrapper:
        write_text_files()
        with open("dexy.yaml", 'w') as f:
            f.write("foo.txt")
        wrapper.run_from_new()

        assert sorted(wrapper.nodes) == ['doc:foo.txt']

def config_txt_single_file_in_subdir__test():
    with wrap() as wrapper:
        write_text_files()
        with open("dexy.yaml", 'w') as f:
            f.write("bar/foo.txt")
        wrapper.run_from_new()

        assert sorted(wrapper.nodes) == ['doc:bar/foo.txt']

def config_txt_wildcard__test():
    with wrap() as wrapper:
        write_text_files()
        with open("dexy.yaml", 'w') as f:
            f.write("\"*foo.txt\"")
        wrapper.run_from_new()

        assert sorted(wrapper.nodes) == [
                'doc:bar/baz/foo.txt',
                'doc:bar/foo.txt',
                'doc:foo.txt',
                'pattern:*foo.txt']


def basic_yaml__test():
    with open(PROJECT_ROOT + "/examples/basic.yaml", 'r') as f:
        yaml = f.read()

    with wrap() as wrapper:
        with open("foo.md", 'w') as f:
            f.write("1 + 1 {{ 1+1 }}")

        with open("example.py", 'w') as f:
            f.write("print 'hello'")

        with open("dexy.yaml", 'w') as f:
            f.write(yaml)

        wrapper.run_from_new()

        assert sorted(wrapper.nodes) == [
                'doc:example.py|pyg',
                'doc:foo.md|jinja|markdown',
                'pattern:*.py|pyg']

        assert "<pre>1</pre>" in str(wrapper.nodes["doc:example.py|pyg"].output_data())
        assert wrapper.nodes["doc:foo.md|jinja|markdown"].setting('output')
