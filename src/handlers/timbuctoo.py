import requests
import json
import sys
import base64

from queries import timbuctoo_queries, timbuctoo_fragments

class Timbuctoo_handler:
    def __init__(self):
        self.server = "https://repository.goldenagents.org/v5/graphql"
        self.tq = timbuctoo_queries.Timbuctoo_queries()
        self.tf = timbuctoo_fragments.Timbuctoo_fragments()
        self.normalized_props = {}
        self.unique_props = {'title': {'shortendedUri': 'title'}}



    def fetch_data(self, query):
        params = {"query": query}
        results = requests.post(self.server, json = params, headers = {'Content-Type': 'application/json',
                                                                       "VRE_ID": "ufab7d657a250e3461361c982ce9b38f3816e0c4b__ecartico_20200316"})
        return json.loads(results.text)

    def get_colls(self, dataset):
        ret_struc = {}
        query = self.tq.get_collections(dataset)
        result = self.fetch_data(query)
        ret_struc["dataSetId"] = result["data"]["dataSetMetadata"]["dataSetId"]
        ret_struc["dataSetName"] = result["data"]["dataSetMetadata"]["dataSetName"]
        ret_struc["items"] =  result["data"]["dataSetMetadata"]["collectionList"]["items"]
        return ret_struc


    def get_props(self, dataset, collection):
        query = self.tq.get_collection_properties(dataset, collection)
        return self.fetch_data(query)

    def get_compact_props(self, dataset, collection):
        ret_struc = {}
        query = self.tq.get_collection_properties(dataset, collection)
        result = self.fetch_data(query)
        ret_struc["uri"] = result["data"]["dataSetMetadata"]["collection"]["uri"]
        ret_struc["shortenedUri"] = result["data"]["dataSetMetadata"]["collection"]["shortenedUri"]
        ret_struc["properties"] = self.get_properties(result["data"]["dataSetMetadata"]["collection"]["properties"]["items"])
        return ret_struc

    def get_properties(self, list):
        ret_list = []
        for item in list:
            buffer = {}
            buffer["uri"] = item["uri"]
            buffer["shortenedUri"] = item["shortenedUri"]
            buffer["density"] = item["density"]
            ret_list.append(buffer)
        return ret_list

    def get_prefixes(self, dataset):
        query = self.tq.get_dataset_prefixes(dataset)
        return self.fetch_data(query)

    def get_metadata(self, dataset):
        query = self.tq.get_metadata(dataset)
        result = self.fetch_data(query)
        result = self.simplify_metadata(result["data"]["dataSets"][dataset]["metadata"])
        result["description"] = result["description"].split('\n')
        return result

    def get_all_metadata(self, store):
        retList = []
        for item in store["dataSets"]:
            print(item["dataSet"])
            md = self.get_metadata(item["dataSet"])
            print(md)
            retList.append({"dataset": item["dataSet"], "metadata": md})
        return retList


    def simplify_metadata(self, md):
        retDict = {}
        for key in md.keys():
            if md[key]:
                if key == 'license' or key == "sparqlEndpoint":
                    retDict[key] = md[key]["uri"]
                else:
                    retDict[key] = md[key]["value"]
            else:
                retDict[key] = ""
        return retDict


    def create_field_query(self, item):
        if item["isList"]:
            if len(item["referencedCollections"]["items"]) > 1:
                return self.tf.entity_list(item["name"])
            else:
                if item["isValueType"]:
                    return self.tf.default_value_list(item["name"])
                else:
                    return self.tf.uri_title_value_list(item["name"])
        else:
            if len(item["referencedCollections"]["items"]) > 1:
                return self.tf.entity(item["name"])
            else:
                if item["isValueType"]:
                    if len(item["referencedCollections"]["items"]) == 1:
                        return self.tf.entity(item["name"])
                    else:
                        return self.tf.default_value(item["name"])
                else:
                    return self.tf.uri_title_value(item["name"])


    def value_extractor(self, props):
        subquery = "title {value} "
        for item in props["data"]["dataSetMetadata"]["collection"]["properties"]["items"]:
            subquery = subquery + self.create_field_query(item)
        return subquery


    def build_query(self, dataset, collection, uri):
        print(collection)
        props = self.get_props(dataset, collection)
        self.normalize_props(props)
        values = self.value_extractor(props)
        query = self.tf.get_item(dataset, collection, uri, values)
        return query

    def normalize_props(self, props):
        # print("<props>")
        # print(props)
        # print("</props>")
        for item in props["data"]["dataSetMetadata"]["collection"]["properties"]["items"]:
            self.normalized_props[item["name"]] = item

    def get_value(self, item):
        if "uri" in item.keys():
            return item["title"]["value"]
        else:
            try:
                return item["value"]
            except:
                return ""

    def humanify_notion(self, field):
        retValue = ""
        #ret_value = field.replace("_inverse_", "")
        #ret_value = ret_value.replace("List", "")
        #ret_value = ret_value.replace("schema_", "")
        if field != 'title':
            if self.normalized_props[field]["shortenedUri"]:
                label = self.normalized_props[field]["shortenedUri"]
            else:
                label = field


            if ":" in label and "http" not in label:
                labelTruncs = label.split(':')
                retValue = labelTruncs[-1]
            else:
                if "#" in label:
                    labelTruncs = label.split("#")
                    retValue = labelTruncs[-1]
                else:
                    retValue = label
        else:
            retValue = field
        return retValue

    def get_field_uri(self, field):
        if field != 'title':
            return self.normalized_props[field]["uri"]
        else:
            return field

    def put_list_values(self, field, data):
        values = []
        for item in data["items"]:
            if "__typename" in item.keys():
                linked_collection = self.get_link(field, item["__typename"])
                if linked_collection != "":
                    params = {
                        "dataset": self.dataset,
                        "collection": linked_collection,
                        "uri": item["uri"]
                    }
                    values.append({"value": self.get_value(item), "link": params})
                else:
                    val = self.get_value(item)
                    if val.startswith("http"):
                        params = {
                            "dataset": "extern",
                            "collection": "",
                            "uri": val
                        }
                        values.append({"value": self.get_value(item), "link": params})
                    else:
                        values.append({"value": self.get_value(item)})
            else:
                values.append({"value": self.get_value(item)})
        return {"notion": field.replace("List", ""), "label": self.humanify_notion(field), "uri": self.get_field_uri(field), "values": values, "type": "human"}


    def get_link(self, field, type_name):
        for col in self.normalized_props[field]["referencedCollections"]["items"]:
            if col != "tim_unknown":
                if col in type_name:
                    return col
        return ""

    def unify_data(self, field, data, pref_list, human = True):
        if data == None:
            return {"notion": field, "label": self.humanify_notion(field), "uri": self.get_field_uri(field), "values": [], "type": "human"}
        else:
            if "items" in data.keys():
                return self.extract_list(field, data)
            else:
                values = []
                if field == "rdf_type" and human:
                    rtype = self.humanize_rdf_type(self.get_value(data))
                    values.append({"value": rtype})
                else:
                    linked_collection = self.get_value_link(field, data)
                    if linked_collection != "":
                        params = {
                            "dataset": self.dataset,
                            "collection": linked_collection,
                            "uri": data["uri"]
                        }
                        values.append({"value": self.get_value(data), "link": params})
                    else:
                        values.append({"value": self.get_value(data)})
                return {"notion": field, "label": self.humanify_notion(field), "uri": self.get_field_uri(field), "values": values, "type": "human"}


    def get_value_link(self, field, data):
        retVal = ""
        if field != 'title' and field != 'uri':
            if "__typename" in data.keys():
                retVal = self.get_link(field, data["__typename"])
        return retVal

    def humanize_rdf_type(self, value):
        type = value.split("/");
        if type[-1]:
            return type[-1]
        else:
            return ""

    def extract_list(self, field, data):
        if field == "rdf_typeList":
            return self.put_rdf_type_list(field, data)
        else:
            return self.put_list_values(field, data)

    def put_rdf_type_list(self, field, data):
        values = []
        for item in data["items"]:
            if "uri" in item.keys():
                rdf_type = item["uri"].split("/")
                obj = {"value": rdf_type[-1]}
                if obj not in values:
                    values.append({"value": rdf_type[-1]})
        return {"notion": field.replace("List", ""), "label": self.humanify_notion(field), "uri": self.get_field_uri(field), "values": values, "type": "human"}

    def model_results(self, dataset, collection, result, list):
        items = []
        for field in result["data"]["dataSets"][dataset][collection]:
            items.append(self.unify_data(field, result["data"]["dataSets"][dataset][collection][field], list))
        return items

    def undouble_items(self, list):
        labels = []
        retList = []
        for item in list:
            if item["label"] not in labels:
                labels.append(item["label"])
            else:
                item["type"] = "rdf"
            retList.append(item)
        return retList

    def rdf_label_as_title(self, title, items):

        if type(title) == str:
            ret_title = title
        else:
            ret_title = title["value"]

        for item in items:
            if item["notion"] == "rdfs_label":
                ret_title = item["values"][0]["value"]
        return ret_title

    def create_adressed_prefixes(self, dataset):
        prefixes = self.get_prefixes(dataset)
        prefixList = {}
        for item in prefixes["data"]["dataSetMetadata"]["prefixMappings"]:
            prefixList[item["uri"]] = item["prefix"]
        return prefixList

    def strip_prefixes(self, dataset, list):
        prefixes = self.get_prefixes(dataset)
        for item in list:
            if item["values"]:
                for i in range(len(item["values"])):
                    value = self.check_prefixes(item["values"][i]["value"], prefixes)
                    if value != item["values"][i]["value"]:
                        item["values"][i]["value"] = value

    def check_prefixes(self, val, prefixes):
        retval = val
        if "http://" in val or "https://" in val:
            for prefix in prefixes["data"]["dataSetMetadata"]["prefixMappings"]:
                if val.startswith(prefix["uri"]):
                    retval = val.replace(prefix["uri"], "")
        return retval


    def get_item(self, dataset, collection, uri):
        self.dataset = dataset
        self.collection = collection
        query = self.build_query(dataset, collection, uri)
        list = self.create_adressed_prefixes(dataset)
        result = self.fetch_data(query)
        items = self.model_results(dataset, collection, result, list)
        tmp = items.pop(0);
        title = tmp["values"][0]
        title = self.rdf_label_as_title(title, items)
        return {"title": title, "uri": uri, "items": items}

    def get_human_item(self, dataset, collection, uri):
        self.dataset = dataset
        self.collection = collection
        query = self.build_query(dataset, collection, uri)
        list = self.create_adressed_prefixes(dataset)
        result = self.fetch_data(query)
        print(query)
        items = self.model_results(dataset, collection, result, list)
        if collection != "schema_Role":
            items = self.undouble_items(items)
        self.strip_prefixes(dataset, items)
        tmp = items.pop(0);
        title = tmp["values"][0]
        title = self.rdf_label_as_title(title, items)
        return {"title": title, "uri": uri, "items": items}