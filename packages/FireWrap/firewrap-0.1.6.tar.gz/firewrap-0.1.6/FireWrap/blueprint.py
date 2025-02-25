from flask import Blueprint, request, jsonify, g, app
from . import FireWrap
import os

firewrap_api = Blueprint("firewrap_api", __name__)

def get_db():
    """Create a new database connection for each request."""
    if 'db' not in g:
        db_name = request.args.get("db", os.getenv("DEFAULT_DB", "firewrap.db"))
        g.db = FireWrap(db_name)
    return g.db

@firewrap_api.route("/collections/<collection>", methods=["GET"])
def get_all_docs(collection):
    db = get_db()
    docs = db.collection(collection).getDocs()
    return jsonify(docs)


@firewrap_api.route("/collections/<collection>", methods=["POST"])
def add_doc(collection):
    db = get_db()
    data = request.json
    doc = db.collection(collection).addDoc(data)
    return jsonify({"message": "Document added", "doc_id": doc.doc_id})

@firewrap_api.route("/collections/<collection>/<doc_id>", methods=["GET"])
def get_doc(collection, doc_id):
    db = get_db()
    doc = db.collection(collection).doc(doc_id).getDoc()
    if doc:
        return jsonify(doc)
    return jsonify({"error": "Document not found"}), 404

@firewrap_api.route("/collections/<collection>/<doc_id>", methods=["POST"])
def new_doc_with_id(collection, doc_id):
    db = get_db()
    data = request.json
    docId = db.collection(collection).addDoc(data, doc_id)
    if docId:
        return jsonify({"message": "Document added", "id": docId})
    return jsonify({"error": "Document not found"}), 404

@firewrap_api.route("/collections/<collection>/<doc_id>", methods=["PATCH"])
def update_doc(collection, doc_id):
    db = get_db()
    data = request.json
    updated = db.collection(collection).doc(doc_id).updateDoc(data)
    if updated:
        return jsonify({"message": "Document updated"})
    return jsonify({"error": "Document not found"}), 404

@firewrap_api.route("/collections/<collection>/<doc_id>", methods=["DELETE"])
def delete_doc(collection, doc_id):
    db = get_db()
    deleted = db.collection(collection).doc(doc_id).deleteDoc()
    if deleted:
        return jsonify({"message": "Document deleted"})
    return jsonify({"error": "Document not found"}), 404

@firewrap_api.route("/collections/<collection>/count", methods=["GET"])
def get_collection_count(collection):
    """Get the total number of documents in a collection."""
    db = get_db()
    count = db.collection(collection).countDocs()
    return jsonify({"count": count})


@firewrap_api.route("/query/<collection>", methods=["GET"])
def query_docs(collection):
    db = get_db()
    filters = request.args.to_dict()
    filters.pop('db', None)
    result = db.collection(collection).queryDocs(**filters)
    return jsonify(result)

@firewrap_api.route("/collections", methods=["GET"])
def get_collection_names():
    db = get_db()
    collections = db.getCollectionNames()  # Assuming this method exists in your FireWrap class
    return jsonify({"collections": collections})

@firewrap_api.route("/collections", methods=["POST"])
def create_collection():
    db = get_db()
    collection_name = request.args.get("name")
    success = db.createCollection(collection_name)
    if success:
        return jsonify({"message": "Collection created", "collection_name": collection_name}), 201
    return jsonify({"error": "Collection could not be created"}), 500
    return jsonify({"collections": collections})
