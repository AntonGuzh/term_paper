import jinja2
import os
import subprocess


async def test(model: dict):
    print(model)


async def compile_tex(model: dict, file: str):
    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('..'))
    )
    template = latex_jinja_env.get_template(file)
    cv = template.render({'model': model})
    with open('tex/res.tex', 'w', encoding='utf-8') as f:
        f.write(cv)

    code = subprocess.call(['pdflatex', 'tex/res.tex'])
    if code:
        return None
    return 'res.pdf'
