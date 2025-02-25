from typing import *

from quicly.mongodb import QxMongoModel, QxMongoClient
from bson import ObjectId


class QxSession(object):
  def __init__(self, session_id: str):
    self._session_id = session_id

  @property
  def session_id(self) -> str:
    return self._session_id

  def __enter__(self):
    self._load()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self._save()

  def _load(self):
    raise NotImplementedError()

  def _save(self):
    raise NotImplementedError()

  def get(self, name: str, default: Any = None) -> Any:
    raise NotImplementedError()

  def set(self, name: str, value: Any):
    raise NotImplementedError()

  def delete(self, name: str):
    raise NotImplementedError()

  def clear(self):
    raise NotImplementedError()


class QxMongoSession(QxSession):
  def __init__(self, model: QxMongoModel, session_id: str):
    super(QxMongoSession, self).__init__(session_id)
    self._model = model

    self._session_data = dict()
    self._session_data_set_table = dict()
    self._session_data_unset_table = dict()

    self._is_loaded = False
    self._is_created = False

  @property
  def model(self) -> QxMongoModel:
    return self._model

  def _load(self):
    self._session_data = dict()
    self._session_data_set_table = dict()
    self._session_data_unset_table = dict()

    self._is_loaded = False
    self._is_created = False

  def _save(self):
    if self._is_created:
      update_table = dict()
      if self._session_data_set_table:
        update_table['$set'] = self._session_data_set_table
      if self._session_data_unset_table:
        update_table['$unset'] = self._session_data_unset_table
      if update_table:
        self.model.update_item_by_pk(QxMongoClient.make_object_id(self.session_id), update_table)
      self._session_data_set_table.clear()
      self._session_data_unset_table.clear()
    else:
      if self._session_data:
        self._session_data['_id'] = QxMongoClient.make_object_id(self.session_id)
        self.model.insert_item(self._session_data)

  def _lazy_load(self):
    if self._is_loaded:
      return

    self._is_loaded = True
    self._session_data = self._model.find_item_by_pk(QxMongoClient.make_object_id(self.session_id))

    if self._session_data:
      self._is_created = True
    else:
      self._session_data = dict()

    for k, v in self._session_data_set_table.items():
      self._session_data[k] = v

    for k in self._session_data_unset_table.keys():
      if k in self._session_data:
        del self._session_data[k]

  def get(self, name: str, default: Any = None) -> Any:
    if name not in self._session_data:
      self._lazy_load()
    return self._session_data.get(name, default)

  def set(self, name: str, value: Any):
    self._session_data[name] = value
    self._session_data_set_table[name] = value
    if name in self._session_data_unset_table:
      del self._session_data_unset_table[name]

  def delete(self, name: str):
    if name in self._session_data:
      del self._session_data[name]
    if name in self._session_data_set_table:
      del self._session_data_set_table[name]
    self._session_data_unset_table[name] = None

  def clear(self):
    self._session_data.clear()
    self._session_data_set_table.clear()
    self._session_data_unset_table.clear()

################################################################################


class QxSessionFactory(object):
  def __init__(self):
    pass

  def new_session_id(self):
    raise NotImplementedError()

  def init_session(self):
    raise NotImplementedError()

  def load_session(self, session_id: str):
    raise NotImplementedError()


class QxMongoSessionFactory(QxSessionFactory):
  def __init__(self, db: Union[QxMongoModel, QxMongoClient]):
    super(QxMongoSessionFactory, self).__init__()
    if isinstance(db, QxMongoModel):
      self._db = db.mongo_client
      self._model = db
    else:
      self._db = db
      self._model = QxMongoModel(db, 'sessions', raw_delete=True)

  @property
  def db(self) -> QxMongoClient:
    return self._db

  @property
  def model(self) -> QxMongoModel:
    return self._model

  def new_session_id(self):
    return str(ObjectId())

  def init_session(self):
    names = self.db.collection_names(include_system_collections=False)
    if self.model.collection_name not in names:
      self.db.create_collection(self.model.collection_name)

  def load_session(self, session_id: str):
    return QxMongoSession(self.model, session_id)
