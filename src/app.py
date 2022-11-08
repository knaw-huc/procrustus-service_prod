from flask import Flask, request, jsonify
import json
from elastic_index import Index
from store import Store
from handlers import timbuctoo
from misc import metadata
import requests


app = Flask(__name__)

config = {
    "url" : "localhost",
    "port" : "9200",
    "doc_type" : "diplo"
}

index = Index(config)
tb = timbuctoo.Timbuctoo_handler()


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Content-type'] = 'application/json'
    return response

@app.route("/")
def hello_world():
    retStruc = {"app": "Procrustus service", "version": "0.1"}
    return json.dumps(retStruc)


@app.route("/facet", methods=['GET'])
def get_facet():
    facet = request.args.get("name")
    amount = request.args.get("amount")
    ret_struc = index.get_facet(facet + ".keyword", amount)
    return json.dumps(ret_struc)

@app.route("/filter-facet", methods=['GET'])
def get_filter_facet():
    facet = request.args.get("name")
    amount = request.args.get("amount")
    facet_filter = request.args.get("filter")
    ret_struc = index.get_filter_facet(facet + ".keyword", amount, facet_filter)
    return json.dumps(ret_struc)

@app.route("/browse", methods=['POST'])
def browse():
    struc = request.get_json()
    ret_struc = index.browse(struc["page"], struc["page_length"], struc["sortorder"] + ".keyword", struc["searchvalues"], struc["collection_index"])
    return json.dumps(ret_struc)

@app.route("/get_store")
def get_store():
    store = Store()
    return json.dumps(store.get_data())

@app.route("/get_metadata_store/<md>")
def get_metadata_store(md):
    store = metadata.MetaData()
    return store.get_metadata(md)

@app.route("/get_metadata/<md>")
def get_metadata(md):
    if md == 'all':
        store = Store()
        data = store.get_data()
        result = tb.get_all_metadata(data)
    else:
        result = tb.get_metadata(md)
    return json.dumps(result)

@app.route("/get_entities/<ds>", methods=["GET"])
def get_entities(ds):
    result = tb.get_colls(ds)
    #query = {"query": result}
    return json.dumps(result)

@app.route("/get_collection_properties/<ds>/<coll>")
def get_properties(ds, coll):
    result = tb.get_props(ds, coll)
    return json.dumps(result)

@app.route("/get_compact_collection_properties/<ds>/<coll>")
def get_compact_properties(ds, coll):
    result = tb.get_compact_props(ds, coll)
    return json.dumps(result)

@app.route("/get_item", methods=["POST"])
def get_item():
    params = request.get_json()
    result = tb.get_item(params["dataset"], params["collection"], params["uri"])
    return json.dumps(result)


@app.route("/get_human_item", methods=["POST"])
def get_human_item():
    params = request.get_json()
    result = tb.get_human_item(params["dataset"], params["collection"], params["uri"])
    return json.dumps(result)


@app.route("/get_prefixes/<ds>")
def get_prefixes(ds):
    result = tb.get_prefixes(ds)
    return json.dumps(result)


@app.get('/typeinfo')
def typeinfo():
    if not request.values.get('url'):
        return 'No url specified', 400

    url = request.values.get('url')
    try:
        res = requests.head(url, allow_redirects=True)
        return jsonify(ok=res.ok,
                       url=url,
                       content_type=res.headers['content-type'] if res.ok else None)
    except:
        return jsonify(ok=False, url=url, content_type=None)


#Start main program

if __name__ == '__main__':
    app.run()

