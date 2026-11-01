import os


def listHtml(folder):
    filesAvailable = os.listdir(folder)
    return filesAvailable


def serveHtml(folder, file):
    htmlContent = ""
    with open(os.path.join(folder, file), encoding="utf-8") as resourceToServe:
        htmlContent  = resourceToServe.read()
    return htmlContent
