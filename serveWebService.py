from flask import Flask, jsonify, request, send_from_directory

from utilsFront import serveHtml, listHtml
from utilsGraph import listResources, listConceptSchemes, extractEntities

app = Flask(__name__)


@app.route("/")
def graphs():
    return serveHtml("frontend", "graphs.html")


@app.route("/visualization")
def map():
    return serveHtml("frontend", "map.html")


@app.route("/hello")
def hello():
    return serveHtml("frontend", "hello.html")


@app.route("/api/graphs")
def apiGraphs():
    return jsonify([f for f in listHtml("graph") if f.endswith(".rdf")])


@app.route("/listResources")
def listResourcesRoute():
    return listHtml("frontend")


@app.route("/api/resources")
def apiResources():
    return jsonify(listResources("graph", request.args.get("graph")))


@app.route("/api/schemes")
def apiSchemes():
    return jsonify(listConceptSchemes("graph", request.args.get("graph")))


@app.route("/api/ner", methods=["POST"])
def apiNer():
    data = request.get_json(force=True)
    return jsonify(extractEntities(data.get("text", "")))


# Fichiers statiques : CSS/JS du frontend, images des ressources et logos
@app.route("/frontend/<path:filename>")
def frontendFiles(filename):
    return send_from_directory("frontend", filename)


@app.route("/ressources/<path:filename>")
def ressources(filename):
    return send_from_directory("ressources", filename)


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("assets", filename)


@app.route("/graph/<path:filename>")
def graphFile(filename):
    return send_from_directory("graph", filename)


if __name__ == "__main__":
    app.run(debug=True)
