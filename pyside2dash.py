# -*- coding: utf-8 -*-
import os
import shutil
import getpass
import logging
import sqlite3
import plistlib

from bs4 import BeautifulSoup

# get version of Qt for Python
soup = BeautifulSoup(open("doc.qt.io/qtforpython/index.html"), "lxml")
title = str(soup.find("div", class_="related").get_text()).strip()
version = title.split(" ")[-1]
docset_folder = "Qt_for_Python.docset"


def get_guides():
    # https://doc.qt.io/qtforpython/contents.html
    soup = BeautifulSoup(open("doc.qt.io/qtforpython/contents.html"), "lxml")
    i = soup.find_all("a", class_="reference internal")
    for x in i:
        # handle 404
        if not str(x["href"]).startswith("https://doc.qt.io"):
            yield (x.get_text(), "Guide", os.path.join("qtforpython", x["href"]))

    # https://doc.qt.io/qtforpython/tutorials/index.html
    soup = BeautifulSoup(open("doc.qt.io/qtforpython/tutorials/index.html"), "lxml")
    i = soup.find_all("a", class_="reference internal")
    for x in i:
        # handle 404
        if not str(x["href"]).startswith("https://doc.qt.io"):
            yield (x.get_text(), "Guide", os.path.join("qtforpython/tutorials", x["href"]))


def get_modules():
    # https://doc.qt.io/qtforpython/modules.html
    soup = BeautifulSoup(open("doc.qt.io/qtforpython/modules.html"), "lxml")
    i = soup.find_all("a", class_="reference internal")
    for x in i:
        # handle 404
        if not str(x["href"]).startswith("https://doc.qt.io"):
            # https://doc.qt.io/qtforpython/PySide2/QtCore/index.html#module-PySide2.QtCore
            t = str(x["href"]).split("#")
            yield (x.get_text(), "Module", os.path.join("qtforpython", t[0]))


def get_classes(modules: list):
    # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractItemDelegate.html
    for m in modules:
        print(m)
        soup = BeautifulSoup(open(os.path.join("doc.qt.io", m[-1])), "lxml")
        i = soup.find_all("a", class_="reference internal")
        for x in i:
            # handle 404
            if not str(x["href"]).startswith("https://doc.qt.io"):
                t = str(x["href"]).split("#")
                if len(t) == 1 or len(t[1]) == 0:
                    yield(x.get_text(), "Class", os.path.join(os.path.dirname(m[-1]), str(x["href"]).strip("#")))


def get_function(classes: list):
    # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractSlider.html#PySide2.QtWidgets.PySide2.QtWidgets.QAbstractSlider.setInvertedControls
    items = {
        "functions": "Function",
        "static-functions": "Function",
        "virtual-functions": "Function",
        "signals": "Provider",
        "slots": "Operator"
    }
    for c in classes:
        soup = BeautifulSoup(open(os.path.join("doc.qt.io", c[-1])), "lxml")
        soup = soup.find("div", class_="body")
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
                            yield(x.get_text(), t, os.path.join(os.path.dirname(c[-1]), x["href"]))


def generate_docset():
    if os.path.exists(docset_folder):
        shutil.rmtree(docset_folder)
    shutil.copytree("doc.qt.io", os.path.join(docset_folder, "Contents/Resources/Documents"))
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


guides = list(get_guides())
modules = list(get_modules())
classes = list(get_classes(modules))
functions = list(get_function(classes))

docs = []
docs.extend(guides)
docs.extend(modules)
docs.extend(classes)
docs.extend(functions)

generate_docset()
write_to_sqlite(docs)
print('Okay! Done! Have fun coding')
