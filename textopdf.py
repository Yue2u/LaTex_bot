from latexcompiler import LC


def make_pdf(tg_id, pr_name):
    path = fr"C:\LaTeX_Bot\UserFiles\{tg_id}\{pr_name}\{pr_name}.tex"
    LC.compile_document(tex_engine='pdflatex',
                        bib_engine='biber',
                        no_bib=True,
                        path=path,
                        folder_name=".aux_files")
