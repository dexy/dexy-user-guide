Here is some python code:

    {{ d['broken.py|pycon'] | assert_does_not_contain("SyntaxError") | indent(4) }}
