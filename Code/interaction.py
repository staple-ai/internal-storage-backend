#!/usr/bin/env python
# coding: utf-8

# In[81]:


from Code.generate_db import dburl
from Code.errors import *
from Code.db_classes import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine, distinct, or_
import magic, os, hashlib, bz2, threading, io






# In[ ]:





# In[83]:



engine = create_engine(dburl)
Session = sessionmaker(bind = engine)
mime = magic.Magic(mime=True)






# This function can be used for adding both documents and folders
def add_element(path, binary = None, force = False):
    
    # Extract filename data
    path = path.strip('/')
    folder, name = os.path.split(path)
    kind = 'folder' if binary is None else 'file'
    
    print("Adding", kind, "element '", name, "' to folder '", folder, "'.")

    session = Session()
    
    # Raise any structural issues
    if get_by_path(path, session) is not None:
        session.close()
        if force:
            print("Deleting existing element for recreate")
            delete_file(path)
        else:
            print("Error: Element with this name already exists")
            raise ElementAlreadyExists()
    if get_by_path(folder, session) is None:
        session.close()
        print("Error: No such folder", folder)
        if force:
            print("Force Add, Adding:", folder)
            add_element(folder, None, True)
        else:
            raise NoSuchFolder()
    
    # Create filepath Structure element
    path = Structure(folder=folder, name=name, kind = kind)
    
    # If adding a file blob
    if binary is not None:
        # Get file type
        filetype = mime.from_buffer(binary) 

        # Get binary hash
        bhash = hashlib.sha256(binary).hexdigest()

        # Check for hash existing in database. If yes, skip get reference and skip til end.
        existing_id = (session
                       .query(Blob.id)
                       .filter(Blob.hashval == bhash)
                       .filter(Blob.kind == filetype)
                       .all()
                      )

        if len(existing_id) > 0:
            # Add to Structure
            print("Found hash in database already:", existing_id[0])
            path.blob_id = existing_id[0]

        else:
            print("Saving Blob to database")
            # Compress binary with bz2.compress
            compressed_binary = bz2.compress(binary)

            # Save binary to Blob table
            blobbymcblobface = Blob(kind = filetype, hashval = bhash, blob = compressed_binary)

            # Add to Structure
            path.blobref = blobbymcblobface
    
    print("Saving item")
    session.add(path)
    session.commit()
    session.refresh(path)
    session.close()
    
    return path.id
    




# In[86]:



# Get id of given path element
def get_by_path(path, session):
    print("Get element info:", path)
    folder, name = os.path.split(path)
    res = (session
           .query(Structure.id, Structure.blob_id, Structure.kind)
           .filter(Structure.folder == folder)
           .filter(Structure.name == name)
           .first()
          )
    return res
    

# Check folder exists
def folder_exists(path, session):
    res = get_by_path(path, session)
    return res is not None and res[2] == 'folder'
# Check file exists
def file_exists(path, session):
    res = get_by_path(path, session)
    return res is not None and res[2] == 'file'

def healtcheck_root_exists():
    session = Session()
    ret = folder_exists('', session)
    session.close()
    return ret


# In[87]:


def flush_blobs():
    print("Flushing unreferenced blobs...")
    session = Session()
    unused_blobs = (session
        .query(Blob.id)
        .join(Structure, isouter = True)
        .filter(Structure.id == None)
        .subquery()
    )
    (session
     .query(Blob)
     .filter(Blob.id.in_(unused_blobs))
     .delete(synchronize_session=False)
    )
    session.commit()
    session.close()
    
    return True



# In[90]:


def get_folder_contents(folder):
    print("Getting contents  of folder", folder)
    folder = folder.strip('/')
    session = Session()
    
    if not folder_exists(folder, session):
        raise NoSuchFolder()
    
    contents = (session
                .query(Structure.name, Structure.kind)
                .filter(Structure.folder == folder)
                .all()
               )
    session.close()
    contents = [{'kind':x[1], 'name': x[0]} for x in contents]
    return contents


# In[91]:


def get_file(filepath):
    print("Getting", filepath, "blob")

    session = Session()

    idx = get_by_path(filepath, session)
    if idx is None or idx[1] is None:
        session.close()
        raise NoSuchFile()
    blob = session.query(Blob).get(idx[1])
    session.close()
    if blob is None:
        raise NoSuchFile({ "message": "Blob Not Found", "item" : filepath})

    print(type(blob.blob))
        
    print("Decompressing...")
    file = bz2.decompress(blob.blob)
    print("Decompressed.")
    return {'file': file, 'mimetype': idx[2], 'name': os.path.split(filepath)[1]}



# In[88]:


def delete_folder(path):
    path = path.strip('/')
    print("Delete folder: ", path)
    folder, name = os.path.split(path)
    session = Session()
    del_contents = (session
              .query(Structure)
              .filter(or_(Structure.folder == path, Structure.folder.startswith(path+'/')))
              .delete(synchronize_session=False)
             )
    print("Deleting",del_contents,"folder contents")
    del_folder = (session
              .query(Structure)
              .filter(Structure.kind == 'folder')
              .filter(Structure.folder == folder)
              .filter(Structure.name == name)
              .delete(synchronize_session=False)
             )
    if del_folder == 0:
        session.rollback()
        session.close()
        raise NoSuchFolder()
    session.commit()
    session.close()
    print("Deleted. Flushing.")
    flush_thread = threading.Thread(target=flush_blobs, name="flusher")
    flush_thread.start()
    return True


# In[89]:


def delete_file(path):
    path = path.strip('/')
    folder, name = os.path.split(path)
    print("Delete file:", path)
    session = Session()
    struct = (session
              .query(Structure)
              .filter(Structure.kind == 'file')
              .filter(Structure.folder == folder)
              .filter(Structure.name == name)
              .first()
             )
    if struct is None:
        raise NoSuchFile()
    
    session.delete(struct)
    session.commit()
    flush_thread = threading.Thread(target=flush_blobs, name="flusher")
    flush_thread.start()
    return True





