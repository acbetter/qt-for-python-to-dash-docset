# Qt for Python (PySide2) to Dash Docset

## Steps

### Download Site

```shell
wget --execute robots=off --wait=0.5 --force-directories --no-parent --page-requisites --mirror --convert-links --tries=3 https://doc.qt.io/qtforpython/
```

### Run the Script

```shell
python pyside2dash.py
```

### Set Icon

- [icon-16px](https://doc.qt.io/style/pyside-16px.png)
- [icon-32px](https://doc.qt.io/style/pyside-32px.png)

### Pack Docset

```shell
tar --exclude='.DS_Store' -cvzf Qt_for_Python.tgz Qt_for_Python.docset
```

## Refer

- [使用 wget 命令进行整站下载](https://m.pythontab.com/article/213)
- [matlab-to-dash-docset](https://github.com/acbetter/matlab-to-dash-docset)

## License

- [Qt for Python](https://doc.qt.io/qtforpython/index.html) use [GNU Free Documentation License version 1.3](https://www.gnu.org/licenses/fdl-1.3.en.html).
- [Qt for Python (PySide2) to Dash Docset](https://github.com/acbetter/qt-for-python-to-dash-docset) use [Apache License Version 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
