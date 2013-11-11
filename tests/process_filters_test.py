from dexy.doc import Doc
from dexy.filter import Filter
from inspect import cleandoc as trim
from utils import wrap
import dexy.load_plugins

def additional_doc_settings_list__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 touch hello.html
                 touch hello.py
                 touch hello.rb
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    additional-doc-filters: {
                        ".py" : "pyg",
                        ".rb" : "pyg"
                    },
                    additional-doc-settings: [
                        [".html", { "data-class" : "bs4" }],
                        [".*", { "ws-template" : "code-template.html" }],
                        ]
                    }
    
            """))

        wrapper.run_from_new()

        assert wrapper.nodes["doc:hello.html"].output_data().alias == 'bs4'
        assert wrapper.nodes["doc:hello.rb|pyg"].setting('ws-template') == "code-template.html"
        assert wrapper.nodes["doc:hello.py|pyg"].setting('ws-template') == "code-template.html"

def additional_doc_settings__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 touch hello.txt
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    additional-doc-settings: {
                        'output' : True,
                        'ws-template' : "custom_template.html"
                        }
                    }
    
            """))

        wrapper.run_from_new()

        doc = wrapper.nodes["doc:hello.txt"]
        assert doc.setting('output') == True
        assert doc.setting('ws-template') == "custom_template.html"


def additional_doc_filters_keep_originals__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 echo "1 + 1 = {{ 1+1 }}" > hello.txt
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    keep-originals: True,
                    additional-doc-filters: "jinja"
                    }
    
            """))

        wrapper.run_from_new()

        assert "doc:hello.txt" in wrapper.nodes

        hello_txt = wrapper.nodes["doc:hello.txt|jinja"]
        assert str(hello_txt.output_data()) == "1 + 1 = 2"

def additional_doc_filters__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 echo "1 + 1 = {{ 1+1 }}" > hello.txt
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    additional-doc-filters: "jinja|ch"
                    }
    
            """))

        wrapper.run_from_new()

        assert not "doc:hello.txt" in wrapper.nodes
        hello_txt = wrapper.nodes["doc:hello.txt|jinja|ch"]
        assert str(hello_txt.output_data()) == "1 + 1 = 2"
        assert hello_txt.output_data().ext == ".html"

def additional_doc_filters_list__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 echo "1 + 1 = {{ 1+1 }}" > hello.txt
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    additional-doc-filters: ["jinja|markdown", "jinja"]
                    }
    
            """))

        wrapper.run_from_new()

        assert not "doc:hello.txt" in wrapper.nodes

        hello_txt = wrapper.nodes["doc:hello.txt|jinja"]
        assert str(hello_txt.output_data()) == "1 + 1 = 2"

        hello_html = wrapper.nodes["doc:hello.txt|jinja|markdown"]
        assert str(hello_html.output_data()) == "<p>1 + 1 = 2</p>"

def additional_doc_filters_dict__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 echo "1 + 1 = {{ 1+1 }}" > hello.txt
                 echo "print 'hello'\n" > example.py
                 touch "foo.rb"
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    additional-doc-filters: {
                        '.txt' : 'jinja',
                        '.py' : ['py', 'pycon|pyg', 'pyg']
                    }
                    }
    
            """))

        wrapper.run_from_new()

        assert not "doc:hello.txt" in wrapper.nodes
        assert "doc:foo.rb" in wrapper.nodes

        assert len(wrapper.nodes) == 6

        hello_txt = wrapper.nodes["doc:hello.txt|jinja"]
        assert str(hello_txt.output_data()) == "1 + 1 = 2"

        example_py_out = wrapper.nodes["doc:example.py|py"]
        assert str(example_py_out.output_data()) == "hello\n"

        example_pycon = wrapper.nodes["doc:example.py|pycon|pyg"]
        assert "&gt;&gt;&gt;" in str(example_pycon.output_data())
        assert "&#39;hello&#39;" in str(example_pycon.output_data())

        example_pyg = wrapper.nodes["doc:example.py|pyg"]
        assert "&#39;hello&#39;" in str(example_pyg.output_data())
        assert not "&gt;&gt;&gt;" in str(example_pyg.output_data())


def populate(yaml):
    with open("script.py", 'w') as f:
        f.write("print 'hello'")

    with open("hello.txt", 'w') as f:
        f.write("1 + 1 = {{ 1+1 }}")

    with open("test.sh", 'w') as f:
        f.write("ls")

    with open("dexy.yaml", 'w') as f:
        f.write(trim(yaml))

def read_result(wrapper):
    result = str(wrapper.nodes['doc:test.sh|sh'].output_data())
    return [l.strip() for l in result.splitlines() if l]

def workspace_exclude_filters_pyg_defaults__test():
    with wrap() as wrapper:
        yaml = """
        - test.sh|sh:
            # Generate a pygments stylesheet.
            - pygments.css|pyg:
                - contents: ""
                - pyg: { 'ext' : '.css' }
            - script.py|pyg
            - script.py|pyg|pn

        """
        populate(yaml)
        wrapper.run_from_new()
        ls_wd = read_result(wrapper)
        assert "pygments.css" in ls_wd
        assert not "script.py.html" in ls_wd
        assert "script.py.png" in ls_wd

def workspace_exclude_filters_excluding_jinja__test():
    with wrap() as wrapper:
        yaml = """
        - test.sh|sh:
            - sh: { workspace-exclude-filters: ['jinja'] }
            - hello.txt|jinja
            - script.py|py
            - script.py|pyg

        """

        populate(yaml)
        wrapper.run_from_new()
        ls_wd = read_result(wrapper)
        assert not "hello.txt" in ls_wd
        assert ls_wd == [
                "script.py.html", # script.py|pyg
                "script.txt", # script.py|py
                "test.sh"]

def workspace_exclude_filters_no_excludes__test():
    with wrap() as wrapper:
        yaml = """
        - test.sh|sh:
            - sh: { workspace-exclude-filters: [] }
            - hello.txt|jinja
            - script.py|py
            - script.py|pyg

        """

        populate(yaml)
        wrapper.run_from_new()
        ls_wd = read_result(wrapper)

        assert ls_wd == [
                "hello.txt", # hello.txt|jinja
                "script.py.html", # script.py|pyg
                "script.txt", # script.py|py
                "test.sh"]

def workspace_exclude_filters_includes_pyg_by_default__test():
    with wrap() as wrapper:
        yaml = """
        - test.sh|sh:
            - hello.txt|jinja
            - script.py|py
            - script.py|pyg

        """

        populate(yaml)
        wrapper.run_from_new()
        ls_wd = read_result(wrapper)

        assert not "script.py.html" in ls_wd
        assert ls_wd == [
                "hello.txt", # hello.txt|jinja
                "script.txt", # script.py|py
                "test.sh"]


def use_wd_option_defaults_to_true__test():
    shint = Filter.create_instance('shint')
    assert shint.setting('use-wd') == True

def if_use_wd_true_code_runs_in_work_dir__test():
    with wrap() as wrapper:
        doc = Doc("test.sh|shint",
                wrapper,
                [],
                contents = "pwd",
                shint = { 'use-wd' : True }
                )

        wrapper.run_docs(doc)
        assert ".dexy/work" in str(doc.output_data())

def if_use_wd_false_code_runs_in_project_home__test():
    with wrap() as wrapper:
        doc = Doc("test.sh|shint",
                wrapper,
                [],
                contents = "pwd",
                shint = { 'use-wd' : False }
                )

        wrapper.run_docs(doc)
        assert not ".dexy/work" in str(doc.output_data())

def mkdir_creates_extra_directory_in_work_dir__test():
    with wrap() as wrapper:
        doc = Doc("test.sh|shint",
                wrapper,
                [],
                contents = "ls -l",
                shint = { 'mkdir' : "foo" }
                )

        wrapper.run_docs(doc)
        foo_line = str(doc.output_data()).splitlines()[2]
        assert foo_line.endswith("foo")
        assert foo_line.startswith("drw")

def mkdirs_creates_extra_directories_in_work_dir__test():
    with wrap() as wrapper:
        doc = Doc("test.sh|shint",
                wrapper,
                [],
                contents = "ls -l",
                shint = { 'mkdirs' : ["foo", "bar"]}
                )

        wrapper.run_docs(doc)
        bar_line = str(doc.output_data()).splitlines()[2]
        foo_line = str(doc.output_data()).splitlines()[3]
        assert foo_line.endswith("foo")
        assert foo_line.startswith("drw")
        assert bar_line.endswith("bar")
        assert bar_line.startswith("drw")

def casperjs_has_add_new_files_true_by_default__test():
    f = Filter.create_instance('casperjs')
    assert f.setting('add-new-files') 

def process_filters_have_add_new_files_false_by_default__test():
    f = Filter.create_instance('process')
    assert not f.setting('add-new-files') 

def if_add_new_files_false_new_files_not_added__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write("touch foo.txt")

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh
    
            """))

        wrapper.run_from_new()
        assert not "doc:foo.txt" in wrapper.nodes.keys()

def if_add_new_files_true_new_files_are_added__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write("touch foo.txt")

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: { add-new-files: True }
    
            """))

        wrapper.run_from_new()
        assert "doc:foo.txt" in wrapper.nodes.keys()

def add_new_files_list__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write("touch foo.txt\ntouch bar.log\nls -l\n")

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: { add-new-files: [.txt] }
    
            """))

        wrapper.run_from_new()

        ls_wd = str(wrapper.nodes['doc:test.sh|sh'].output_data())
        assert "bar.log" in ls_wd
        assert "foo.txt" in ls_wd

        assert "doc:foo.txt" in wrapper.nodes.keys()
        assert not "doc:bar.log" in wrapper.nodes.keys()

def add_new_files_pattern__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write("touch foo.txt\ntouch bar.log\ntouch other.log\nls -l\n")

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: { add-new-files: ["b*.log"] }
    
            """))

        wrapper.run_from_new()

        ls_wd = str(wrapper.nodes['doc:test.sh|sh'].output_data())
        assert "foo.txt" in ls_wd
        assert "bar.log" in ls_wd
        assert "other.log" in ls_wd

        assert not "doc:foo.txt" in wrapper.nodes.keys()
        assert "doc:bar.log" in wrapper.nodes.keys()
        assert not "doc:other.log" in wrapper.nodes.keys()

def exclude_add_new_files__test():
    with wrap() as wrapper:
        with open("test.sh", 'w') as f:
            f.write(trim("""\
                 touch foo.txt
                 touch bar.log
                 touch foo/hello.txt
                 ls -l"""))

        with open("dexy.yaml", 'w') as f:
            f.write(trim("""
            - test.sh|sh:
                - sh: {
                    add-new-files: True,
                    exclude-add-new-files: ["foo"]
                    }
    
            """))

        wrapper.run_from_new()

        ls_wd = str(wrapper.nodes['doc:test.sh|sh'].output_data())
        assert "foo.txt" in ls_wd
        assert "bar.log" in ls_wd

        assert not "doc:foo.txt" in wrapper.nodes.keys()
        assert "doc:bar.log" in wrapper.nodes.keys()
