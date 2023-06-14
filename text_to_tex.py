from pylatex import Command, Document, Section
from pylatex.package import Package
from pylatex.utils import NoEscape
from create_bot import USER_DATA
from utils import path_join
import json
import os


# На устройстве на котором стоит бот должен быть установлен например полный TeXLive, чтобы в pdf компилировать


def add_section(uid: int, pr_name: str, title: str, paragraphs: list):
    section = Document(
        documentclass="subfiles", document_options=[NoEscape("../main.tex")]
    )
    section.packages.append(Package("subfiles"))

    # пока умеем только прикреплять параграфы с текстом
    with section.create(Section(title)):
        for par in paragraphs:
            section.append(par)
            section.append(Command(command="par"))

    # если добавляем первый раздел, то автоматически создадутся нужная папка и json
    path = path_join(USER_DATA, uid, pr_name, "sections")
    if os.path.exists(path):
        with open(
            path_join(USER_DATA, uid, pr_name, "jsons", "sectionlist.json"), "r"
        ) as f:
            sectionlist = json.load(f)
    else:
        os.mkdir(path)
        sectionlist = []

    section.generate_tex(
        path_join(USER_DATA, uid, pr_name, "sections", len(sectionlist))
    )
    sectionlist.append(title)

    with open(
        path_join(USER_DATA, uid, pr_name, "jsons", "sectionlist.json"), "w"
    ) as f:
        json.dump(sectionlist, f, indent=4, ensure_ascii=False)


def build_document(uid: int, pr_name: str):
    with open(path_join(USER_DATA, uid, pr_name, "jsons", "config.json"), "r") as f:
        params = json.load(f)
    fontsize = params["font_size"]
    margin = params["indent"]
    project = Document(
        documentclass="extarticle", fontenc="T1, T2A", document_options=f"{fontsize}pt"
    )
    project.packages.append(Package("extsizes"))
    project.packages.append(Package("geometry", options=f"a4paper,margin={margin}mm"))
    project.packages.append(
        Package("indentfirst")
    )  # добавляет отступ у первого параграфа раздела
    project.packages.append(Package("subfiles"))
    project.packages.append(Package("babel", options="russian,english"))
    project.preamble.append(Command("title", pr_name))
    project.append(NoEscape(r"\maketitle"))

    # Example
    # with project.create(Section("Это раздел из основного документа")):
    #     project.append("Проверка русского текста. Этот раздел можно убрать. ")
    #     project.append("Дальше идут разделы добавленные с помощью add_section")

    with open(
        path_join(USER_DATA, uid, pr_name, "jsons", "sectionlist.json"), "r"
    ) as f:
        sectionlist = json.load(f)

    n = len(sectionlist)
    for i in range(n):
        project.append(
            Command(command="subfile", arguments=NoEscape(f"./sections/{i}.tex"))
        )

    project.generate_tex(path_join(USER_DATA, uid, pr_name, pr_name))
    project.generate_pdf(path_join(USER_DATA, uid, pr_name, pr_name), clean_tex=False)


# Example
if __name__ == "__main__":
    user_id = 308
    project_name = "Bebrology 1"

    # если запускать несколько раз подряд, то эти два раздела будут прикрепляться к концу, не заменяя старые
    add_section(
        user_id,
        project_name,
        "Subfile moment",
        [
            "This is text contained in the first paragraph of the first section. "
            "This is text contained in the first paragraph of the first section. "
            "This is text contained in the first paragraph of the first section. ",
            "This is text contained in the second paragraph of the first section. "
            "This is text contained in the second paragraph of the first section. "
            "This is text contained in the second paragraph of the first section. ",
            "Третий параграф на русском. Другие языки работают и в подразделах.",
        ],
    )

    add_section(
        user_id,
        project_name,
        "Subfile moment sequel",
        [
            "And in the second section there are only two paragraphs. "
            "And in the second section there are only two paragraphs. "
            "And in the second section there are only two paragraphs. ",
            "The second paragraph of the second section. "
            "The second paragraph of the second section. "
            "The second paragraph of the second section",
        ],
    )

    build_document(user_id, project_name)
