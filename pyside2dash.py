# -*- coding: utf-8 -*-


import os
import shutil
import logging
import sqlite3
import plistlib
from multiprocessing import Pool

from bs4 import BeautifulSoup


docset_folder = "./Qt_for_Python.docset"
num_worker = 16


# guides_1
def get_guides_1():
    # https://doc.qt.io/qtforpython/index.html
    soup = BeautifulSoup(open("./doc.qt.io/qtforpython/index.html"), "lxml")
    i = soup.find_all("li", class_="toctree-l1")
    for x in i:
        line = x.contents[0]
        if not str(line["href"]).startswith("https://doc.qt.io"):
            yield line.get_text(), "Guide", os.path.join("qtforpython", line["href"])


# guides_2
def get_guides_2():
    # https://doc.qt.io/qtforpython/index.html
    soup = BeautifulSoup(open("./doc.qt.io/qtforpython/index.html"), "lxml")
    i = soup.find_all("li", class_="toctree-l2")
    for x in i:
        line = x.contents[0]
        if not str(line["href"]).startswith("https://doc.qt.io"):
            yield line.get_text(), "Guide", os.path.join("qtforpython", line["href"])


# guides_3
def get_guides_3():
    # https://doc.qt.io/qtforpython/index.html
    soup = BeautifulSoup(open("./doc.qt.io/qtforpython/index.html"), "lxml")
    i = soup.find_all("li", class_="toctree-l3")
    for x in i:
        line = x.contents[0]
        if not str(line["href"]).startswith("https://doc.qt.io"):
            if "tutorials" in line["href"]:
                yield line.get_text(), "Guide", os.path.join("qtforpython", line["href"])


# modules
def get_modules():
    # https://doc.qt.io/qtforpython/index.html
    soup = BeautifulSoup(open("./doc.qt.io/qtforpython/index.html"), "lxml")
    i = soup.find_all("li", class_="toctree-l3")
    for x in i:
        line = x.contents[0]
        if not str(line["href"]).startswith("https://doc.qt.io"):
            if "tutorials" not in line["href"]:
                yield line.get_text(), "Module", os.path.join("qtforpython", line["href"])


# classes
def get_classes():
    # https://doc.qt.io/qtforpython/index.html
    soup = BeautifulSoup(open("./doc.qt.io/qtforpython/index.html"), "lxml")
    i = soup.find_all("li", class_="toctree-l4")
    for x in i:
        line = x.contents[0]
        if not str(line["href"]).startswith("https://doc.qt.io"):
            yield line.get_text(), "Class", os.path.join("qtforpython", line["href"])


# function
def functions_single(c):
    items = {
        "functions": "Function",
        "static-functions": "Function",
        "virtual-functions": "Function",
        "signals": "Provider",
        "slots": "Operator",
        "id3": "Function"
    }
    res_ = []
    soup = BeautifulSoup(open(os.path.join("./doc.qt.io", c[-1])), "lxml")
    soup = soup.find("body")
    synopsis = soup.find(id="synopsis")
    if not synopsis:
        logging.warning("{} don't have synopsis".format(c))
    else:
        for tag in synopsis.find_all(True):
            if tag.has_attr("id"):
                if tag["id"] in items.keys():
                    t = items[tag["id"]]
                else:
                    t = "Function"
                    logging.warning("ID {} don't exist in records.".format(tag["id"]))
                i = tag.find_all("a", class_="reference internal")
                for x in i:
                    # handle 404
                    if not str(x["href"]).startswith("https://doc.qt.io"):
                        res_.append((x.get_text(), t, os.path.join(os.path.dirname(c[-1]), x["href"])))

    return res_


# deduplicate
def deduplicate(items: list, name: str):
    set_items = set(items)
    print('The number of {} is {}, and the number is {} after removing duplicated items.'
          .format(name, len(items), len(set_items)))
    return list(set_items)


def get_functions(classes: list):
    with Pool(num_worker) as p:
        res = p.map(functions_single, classes)
    res = [item for items in res for item in items]

    return res


def generate_docset():
    if os.path.exists(docset_folder):
        shutil.rmtree(docset_folder)
    shutil.copytree("./doc.qt.io", os.path.join(docset_folder, "Contents/Resources/Documents"))
    info_plist = dict(
        CFBundleIdentifier="qtforpython",
        CFBundleName="Qt for Python",
        DocSetPlatformFamily="qtforpython",
        isDashDocset=True,
        dashIndexFilePath="qtforpython/index.html",
        isJavaScriptEnabled=True
    )
    with open(os.path.join(docset_folder, "Contents/Info.plist"), "wb") as f:
        plistlib.dump(info_plist, f)


def write_to_sqlite(doc_set: list):
    print('Writing to sqlite.... It may take seconds... Please wait...')
    conn = sqlite3.connect(os.path.join(docset_folder, 'Contents/Resources/docSet.dsidx'))
    cur = conn.cursor()
    try:
        cur.execute('DROP TABLE searchIndex;')
    except sqlite3.OperationalError:
        pass
    cur.execute('CREATE TABLE searchIndex (id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    for item in doc_set:
        cur.executemany('INSERT OR IGNORE INTO searchIndex (name, type, path) VALUES (?,?,?)', [item])
        print(item, end='\n')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    guides_1 = list(get_guides_1())
    guides_2 = list(get_guides_2())
    guides_3 = list(get_guides_3())
    guides = []
    guides.extend(guides_1)
    guides.extend(guides_2)
    guides.extend(guides_3)
    guides = deduplicate(guides, 'guides')

    modules = list(get_modules())
    modules = deduplicate(modules, 'modules')

    classes = list(get_classes())
    classes = deduplicate(classes, 'classes')

    functions = get_functions(classes)
    functions = deduplicate(functions, 'functions')

    docs = []
    docs.extend(guides)
    docs.extend(modules)
    docs.extend(classes)
    docs.extend(functions)

    generate_docset()
    write_to_sqlite(docs)
    print('Okay! Done! Have fun coding')
