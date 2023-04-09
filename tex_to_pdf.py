from latexcompiler import LC


async def make_pdf(path):
    LC.compile_document(
        tex_engine="pdflatex",
        bib_engine="biber",
        no_bib=True,
        path=path,
        folder_name=".aux_files",
    )
