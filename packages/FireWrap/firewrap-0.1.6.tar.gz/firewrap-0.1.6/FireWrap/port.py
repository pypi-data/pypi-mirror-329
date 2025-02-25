import firebase_admin
from firebase_admin import credentials, firestore
from FireWraper.FireWrap import FireWrap
import traceback

def migrate_firebase_to_local_sql(firebase_json_path, db_name="firesql.db", collections_to_migrate=[]):
    """
    Migrate documents from Firebase to FireSQL.

    Args:
        firebase_json_path (str): Path to Firebase credentials JSON file
        db_name (str): Name of the FireSQL database file
        collections_to_migrate (list): List of Firebase collection names.
                                     If empty ( [] ), migrate all collections.
    """
    try:
        cred = credentials.Certificate(firebase_json_path)
        firebase_admin.initialize_app(cred)
        firebase_db = firestore.client()

        if not collections_to_migrate:
            collections_to_migrate = get_all_firestore_collections(firebase_db)

        firesql_db = FireWrap(f"sqlite:///{db_name}")

        for collection_name in collections_to_migrate:
            print(f"Migrating '{collection_name}'...")

            firesql_collection = firesql_db.collection(collection_name)

            docs = firebase_db.collection(collection_name).stream()

            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                firesql_collection.doc(doc.id).setDoc(data)

            print(f"Successfully migrated '{collection_name}'!")

        firesql_db.close()
        print("Migration complete!")

    except Exception as e:
        print(f"Error during migration: {e}")
        print(traceback.format_exc())
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())

def get_all_firestore_collections(firebase_db):
    """
    Retrieve all collection names from Firebase Firestore.
    
    Args:
        firebase_db: Firestore client instance
    """
    collections = firebase_db.collections()
    return [col.id for col in collections]
