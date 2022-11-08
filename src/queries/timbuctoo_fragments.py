class Timbuctoo_fragments:
    def default_value(self, field):
        return " " + field + " { ... on Value {value} } "

    def default_value_list(self, field):
        return " " + field + " {items {... on Value {value}}} "

    def entity(self, field):
        #if "inverse_" in field:
            return " " + field + " {... on Entity {uri title { ... on Value {value type __typename}} __typename}} "
        #else:
        #    return " " + field + " {... on Entity {uri title { ... on Value {value type __typename}} __typename} ... on Value {value type}} "

    def entity_list(self, field):
        return " " + field + " {items { ... on Entity {uri title { ... on Value {value type __typename}} __typename}}} "

    def uri_title_value(self, field):
        return " " + field + " { uri title {value} __typename} "

    def uri_title_value_list(self, field):
        return " " + field + " {items {uri title {value} __typename}} "

    def get_item(self, dataset, collection, uri, fields):
        return "{dataSets {" + dataset + " {" + collection + '(uri: "' + uri + '") {' + fields + "}}}}"
