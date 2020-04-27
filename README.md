# Qt for Python (PySide2) to Dash Docset

## Steps

### Download Site

It may take about 1 hour. You can change `--wait=0.5` but better don't do this.

```shell
wget --execute robots=off --wait=0.5 --force-directories --no-parent --page-requisites --mirror --convert-links --tries=3 https://doc.qt.io/qtforpython/
```

```shell
Here is my example running result.
FINISHED --2020-04-27 15:31:39--
Total wall clock time: 1h 6m 16s
Downloaded: 4449 files, 105M in 3m 45s (477 KB/s)
```

### Run the Script

You need install python3 and `pip install -r requirements.txt` first.

```shell
python pyside2dash.py
```

### Set Icon

Manually download/copy this to your docset folder.

- [icon-16px](https://doc.qt.io/style/pyside-16px.png) to icon.png
- [icon-32px](https://doc.qt.io/style/pyside-32px.png) to icon@2x.png

### Pack Docset

```shell
tar --exclude='.DS_Store' -cvzf Qt_for_Python.tgz Qt_for_Python.docset
```

## Refer

- [使用 wget 命令进行整站下载](https://m.pythontab.com/article/213)
- [matlab-to-dash-docset](https://github.com/acbetter/matlab-to-dash-docset)

## Contributor

- [Oliver Kletzmayr](https://github.com/okletzmayr)

## License

- [Qt for Python Documentation](https://doc.qt.io/qtforpython/index.html) use [GNU Free Documentation License version 1.3](https://www.gnu.org/licenses/fdl-1.3.en.html)
- [Qt for Python (PySide2) to Dash Docset](https://github.com/acbetter/qt-for-python-to-dash-docset) use [Apache License Version 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
