import json

class MetaData:

    def __init__(self):
        self.metadata = {
            "u692bc364e9d7fa97b3510c6c0c8f2bb9a0e5123b__rijksmuseum" : {
                        "title": "Rijksmuseum Collection",
                        "description": "This dataset is a copy of the Europeana Data Model dump of the Rijksmuseum Collection data that can be downloaded at https://data.rijksmuseum.nl/object-metadata/download/. \n\nThe data published by the Golden Agents project is a copy dated 17th February 2021 - the only editing done is replacing the AAT-Ned Thesaurus, http://www.aat-ned.nl/ (offline and lost since 16-11-2020) with the Getty AAT Thesaurus, http://vocab.getty.edu/aat/.",
                        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/6/67/Rijks_museum_logo.png",
                        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                        "publisher": "Golden Agents project",
                        "creator": "Rijksmuseum",
                        "contributor": "",
                        "dataProvider": "Rijksmuseum",
                        "subject": "",
                        "source": "https://data.rijksmuseum.nl/object-metadata/download/",
                        "created": "2021-02-17",
                        "modified": "2021-02-17",
                        "sparqlEndpoint": ""
                    },
            "u692bc364e9d7fa97b3510c6c0c8f2bb9a0e5123b__stcn" :  {
                "title": "Short-Title Catalogue Netherlands (STCN)",
                "description": "Expert descriptions of books printed in the Netherlands between 1473 and 1801 in more than 210.000 editions in 550.000 copies. Contains descriptions of books in the collections of many libraries in the Netherlands and various libraries abroad. All books are described book in hand. Descriptions contain information about authors, titles, imprints, size, collation formula, subject keywords and typographical features. Every edition is distinguished by the STCN fingerprint. Newspapers and ambassadors’ letters are excluded. \n\nThis dataset is a https://schema.org/ copy of the STCN datadump (http://data.bibliotheken.nl/id/dataset/stcn), the STCN Printers (http://data.bibliotheken.nl/id/dataset/stcn/printers) and the STCN Thesauri (http://data.bibliotheken.nl/id/dataset/stcn/thes) from 2022-04-29. ",
                "imageUrl": "https://www.kb.nl/kbhtml/stcnhandleiding/logo.jpg",
                "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                "publisher": "Golden Agents project",
                "creator": "Koninklijke Bibliotheek",
                "contributor": "Golden Agents project",
                "dataProvider": "Koninklijke Bibliotheek",
                "subject": "book production",
                "source": "http://data.bibliotheken.nl/id/dataset/stcn",
                "created": "2022-04-29",
                "modified": "2022-04-29",
                "sparqlEndpoint": ""
            },
            "u692bc364e9d7fa97b3510c6c0c8f2bb9a0e5123b__schrijverskabinet": {
                "title": "Schrijverskabinet",
                "description": "The Panpoëticon Batavûm is a collection of small portraits of Dutch poets (and writers in general). The collection was set up at the beginning of the eighteenth century by the painter Arnoud Halen (1673-1732). As a collection the Panpoëticon is no longer intact, but fortunately a digital reconstruction can be seen at http://www.schrijverskabinet.nl/. This dataset offers a RDF version of this website, so that one can connect the entities that are included in the Schrijverskabinet to other relevant datasets that for instance include more detailed biographical information, such as ECARTICO, ONSTAGE, and Wikidata.\n\nIn this version, all URIs that were prefixed on https://data.create.humanities.uva.nl/id/ are replaced by https://data.goldenagents.org/datasets/. This is a https://schema.org version of the data.\n\nFor more information on this dataset or for citation, please refer to the paper: Nijboer, H., van Deinsen, L., van Wissen, L., Brouwer, J., van Strien, T., & Blom, F. (2021). Using Linked Data to Track and Trace Processes of Canonization in early Modern Dutch Literature. DH Benelux Journal, 3, 39-59. https://doi.org/10.17613/p3z7-4c05",
                "imageUrl": "http://www.schrijverskabinet.nl/wp-content/uploads/2015/10/tijdlijn-onderhandse-verkoop.jpg",
                "license": "https://creativecommons.org/licenses/by-sa/4.0/",
                "publisher": "Golden Agents project",
                "creator": "Harm Nijboer, Leon van Wissen",
                "contributor": "Lieke van Deinsen, Ton van Strien",
                "dataProvider": "http://schrijverskabinet.nl/",
                "subject": "canonization",
                "source": "https://doi.org/10.5281/zenodo.4727106",
                "created": "2020-05-29",
                "modified": "2021-04-29",
                "sparqlEndpoint": ""
            },
            "u692bc364e9d7fa97b3510c6c0c8f2bb9a0e5123b__notarissennetwerk" : {
                "title": "Notarissen netwerk",
                "description": "Description upcoming..",
                "imageUrl": "http://www.schrijverskabinet.nl/wp-content/uploads/2015/10/tijdlijn-onderhandse-verkoop.jpg",
                "license": "https://creativecommons.org/licenses/by-sa/4.0/",
                "publisher": "Upcoming..",
                "creator": "Upcoming..",
                "contributor": "Upcoming..",
                "dataProvider": "Upcoming..",
                "subject": "Upcoming..",
                "source": "Upcoming..",
                "created": "2020-05-29",
                "modified": "2021-04-29",
                "sparqlEndpoint": ""
            },
            "u692bc364e9d7fa97b3510c6c0c8f2bb9a0e5123b__jaikwil" : {
                "title": "Ja, ik wil!",
                "description": "Description upcoming..",
                "imageUrl": "http://www.schrijverskabinet.nl/wp-content/uploads/2015/10/tijdlijn-onderhandse-verkoop.jpg",
                "license": "https://creativecommons.org/licenses/by-sa/4.0/",
                "publisher": "Upcoming..",
                "creator": "Upcoming..",
                "contributor": "Upcoming..",
                "dataProvider": "Upcoming..",
                "subject": "Upcoming..",
                "source": "Upcoming..",
                "created": "2020-05-29",
                "modified": "2021-04-29",
                "sparqlEndpoint": ""
            }
        }

    def get_metadata(self, set):
        if set == "all":
            return json.dumps(self.send_metadata_list())
        try:
            return json.dumps(self.metadata[set])
        except:
            return json.dumps({})

    def send_metadata_list(self):
        retArray = []
        for key in self.metadata.keys():
            buffer = {}
            buffer["dataset"] = key
            buffer["metadata"] = self.metadata[key]
            retArray.append(buffer)
        return retArray
