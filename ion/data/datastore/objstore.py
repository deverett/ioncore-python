#!/usr/bin/env python
"""
@file ion/data/datastore/objstore.py
@author Dorian Raymer
@author David Stuebe
@author Michael Meisinger
"""

import logging

from zope import interface

from twisted.internet import defer
from twisted.python import reflect

from ion.data.datastore import cas

NULL_CHR = '\x00'

class ObjectStoreError(Exception):
    """
    Base ObjectStore Exception
    """

class IObjectChassis(interface.Interface):
    """
    A vehicle for carrying an application object in and out of
    the Object Store.

    The concept is very similar to a git repository.
    """

    def get_head(name):
        """
        """

    def update_head(commit_id, name):
        """
        """

    def checkout(ref):
        """
        """

    def commit():
        """
        """

    def write_tree():
        """
        """


class IObjectStore(cas.ICAStore):
    """
    A CAStore for data objects.
    """

    def create(name, baseClass):
        """
        @brief Create a new data object entity with the structure of
        baseClass.
        @param name Unique identifier of data object.
        @param baseClass Class that models structure of data object. This
        class is a container of typed attributes.
        """

    def clone(name):
        """
        @brief Retrieve data object.
        @param name Unique identifier of data object.
        """

class TypedAttribute(object):
    """
    @brief Descriptor class for Data Object Attributes. Objects are
    containers of typed attributes.
    """

    def __init__(self, type, default=None):
        self.name = None
        self.type = type
        self.default = default if default else type()
        self.cache = None

    def __get__(self, inst, cls):
        value = getattr(inst, self.name, self.default)
        return value

    def __set__(self, inst, value):
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s" % self.type)
        setattr(inst, self.name, value)

    @classmethod
    def decode(cls, value):
        stype, default = value.split(NULL_CHR)
        
        type = eval(str(stype))
#        return cls(type, type(str(default)))

        if type == list:
            return cls(type, eval(str(default)))
        else:
           return cls(type, type(str(default)))

class StoreType(type):
    """
    @brief Metaclass for all Data Objects.
    """

    def __new__(cls, name, bases, dict):
        slots = []
        for key, value in dict.items():
            if isinstance(value, TypedAttribute):
                value.name = '_' + key
                slots.append(value.name)
        dict['__slots__'] = slots
        return type.__new__(cls, name, bases, dict)

class StoreClass(object):
    """
    @brief [Abstract] Base class for all data objects.
    """
    __metaclass__ = StoreType

    def __eq__(self,other):
        
        if not isinstance(other, BaseResource):
            return False
        
        for name in self.attributes:
            self_value = getattr(self,name)
            
            other_value = getattr(other,name)
            if other_value != self_value:
                return False
        return True

    def __str__(self):
        head = '='*10
        strng  = """\n%s Resource Type: %s %s\n""" % (head, str(self.__class__.__name__), head)
        for name in self.attributes:
            value = getattr(self,name)
            strng += """= '%s':'%s'\n""" % (name,value)
        strng += head*2
        return strng

    @property
    def attributes(self):
        names = []
        for key in self.__slots__:
            names.append(key[1:])
        return names

    def encode(self):
        """
        """
        encoded = []
        for name in self.attributes:
            value = getattr(self, name)
            
            # Attempt to handle nested Resources
            if not isinstance(value, StoreClass):
                encoded.append((name, "%s%s%s" % (type(value).__name__, NULL_CHR, str(value),)))
            else:
                value = value.encode()
                encoded.append((name, "%s%s%s" % (type(value).__name__, NULL_CHR, str(value),)))
        return encoded

    @classmethod
    def decode(cls, className, attrs):
        """
        decode store object[s]
        """
        #d = dict([(str(name), TypedAttribute.decode(value)) for name, value in attrs])
        d={}
        for name, value in attrs:
            #print 'name',name
            #print 'value',value
            d[str(name)] = TypedAttribute.decode(value)       
        return type(str(className), (cls,), d)

class EmptyObject(StoreClass):
    """
    @brief Trivial Store Object
    """

class ArbitraryObject(StoreClass):
    key = TypedAttribute(str)


class Element(cas.Element):

    def load(self, backend):
        """
        @brief experimental way to dynamically load objects from id's.
        """
        if not self.obj:
            def cb(obj):
                self.obj = obj
                return obj.load(backend)

            d = backend.get(self[1])
            d.addCallback(cb)
            return d
        return defer.succeed(None)


class Blob(cas.Blob):

    def __repr__(self):
        return self.content

    def load(self, backend):
        """
        @brief leaf of load recursion. Do nothing.
        """
        return defer.succeed(self.content)

class Tree(cas.Tree):

    elementFactory = Element

    def load(self, backend):
        """
        @brief Call load on all entities.
        """
        return defer.DeferredList([child.load(backend) for child in self.children])

    def x__getitem__(self, name):
        """
        lazy loading
        """

class Commit(cas.Commit):

    def load(self, backend, recursive=False):
        """
        """
        if not self.tree_obj:
            d = backend.get(self.tree)
            def cb(obj):
                self.tree_obj = obj
                if recursive:
                    return obj.load(backend)
            d.addCallback(cb)
            return d
        return defer.succeed(None)

class UUID(Blob):
    """
    Names of objects are UUIDs and are stored as content objects.
    """

    type = 'uuid'

class ObjectStoreObject(Tree):
    """
    @brief An ObjectStore Object is the main entity of the ObjectStore
    environment.
    """

    type = 'object' # or 'entity'?


class BaseObjectChassis(object):
    """
    Creation functionality of ObjectChassis. 
    This base cla
    """

    def __init__(self, objstore, keyspace, objectClass=StoreClass):
        """
        @note
        objstore vs. objs
        objstore implements ICAStore; objs is just the raw key/value
        (namespaced) interface to the content objects.
        refs is not a refstore (yet); it is just the namespaced key/value
        store for accessing the refs. Same for meta.
        objstore expects/returns cas.BaseObject types
        refs & meta don't necessarily have types (yet).
        """
        self.objstore = objstore
        self.keyspace = keyspace
        self.objectClass = objectClass
        self.index = None
        self.cur_commit = None

    @classmethod
    def new(cls, objstore, keyspace, objectClass):
        """
        @todo Design for recording 'objectClass' in system.
        @todo How to organize creation of refs, meta, etc.
        """
        inst = cls(objstore, refs, meta, objectClass)
        return inst


    def _get_object_meta(self):
        """
        @brief Common meta info on this object.
        It's like the misc mutable stuff in .git
        """
        d = self.meta.get('')

        def _raise_if_none(res):
            if not bool(res):
                raise ObjectStoreError("Store meta not found")
            return res
        d.addCallback(_raise_if_none)
        return d

class ObjectChassis(BaseObjectChassis):
    """
    This establishes a context for accessing/modifying/committing an
    "Object" or "Resource Entity" structure...thing.
    """

    def update_head(self, commit_id, head='master'):
        """
        @param commit_id Id of CAStore commit object.
        @brief Update association of reference name to commit id.
        In general, head is a ref, but other refs are not yet implemented.
        @retval Deferred
        """
        return self.keyspace.put('refs.' + head, commit_id)

    def get_head(self, name='master'):
        """
        @brief Get reference named 'name'. The head references represent
        commit ancestry chains. Master is the name of the main commit
        linage. A branch is represents a divergent commit linage. Any head
        reference besides the one named 'master' is a branch head.
        @retval commit object id
        @todo get('heads.master') instead of just get('head')
        @note if head is not there, *IStore says return None*
        """
        return self.keyspace.get('refs.' + name)

    @defer.inlineCallbacks
    def checkout(self, head='master', commit_id=None):
        """
        """
        if commit_id:
            ref = commit_id
        else:
            ref = yield self.get_head(head)
        if ref:
            commit = yield self.objstore.get(ref)
            tree = yield self.objstore.get(commit.tree)
            yield tree.load(self.objstore)
            obj_parts = [(child[0], child.obj.content) for child in tree.children]
            obj_class_name = yield self.meta.get('objectClass')
            self.index = self.objectClass.decode(obj_class_name, obj_parts)()
        else:
            self.index = self.objectClass()
        self.cur_commit = ref
        defer.returnValue(self.index)

    @defer.inlineCallbacks
    def write_tree(self):
        """
        write current index
        """
        obs = self.index.encode()
        blobs = [(name, Blob(val)) for name, val in obs]
        for n, b in blobs:
            yield self.objstore.put(b)
        childs = [Element(name, blob) for name, blob in blobs]
        tree = Tree(*childs)
        tree_id = yield self.objstore.put(tree)
        defer.returnValue(tree_id)

    def write_blob(self, val):
        return self.objstore.put(Blob(val))
        
    def add(self, element):
        """
        @param entity Instance of Element or ElementProxy.
        """

    def update(self, element):
        """
        """

    def remove(self, element):
        """
        """

    @defer.inlineCallbacks
    def commit(self, working_tree=None):
        """
        """
        id = yield self.write_tree()
        if self.cur_commit:
            parents = [self.cur_commit]
        else:
            parents = []
        commit = Commit(id, parents)
        commit_id = yield self.objstore.put(commit)
        yield self.update_head(commit_id)
        defer.returnValue(commit_id)

    @defer.inlineCallbacks
    def get_commit_history(self):
        commits = []
        id = yield self.get_head()
        if not id:
            defer.returnValue([])
        while True:
            c = yield self.objstore.get(id)
            commits.append(c)
            if c.parents:
                # ignore multiples...
                id = c.parents[0]
                continue
            break
        defer.returnValue(commits)

class BaseObjectStore(cas.CAStore):
    """
    @brief Interactive interface to an Object Store instance (who's raw
    data lives on some 'backend'. An instance of this object sets the
    context for creating/modifying/retrieving "Object" or "Resource
    Entity" structures from a general key/value store. Each structure is
    accessed by a UUID. 
     - Each structure is comparable to a git repository
    Each structure is a model composed of references to content objects
    (blobs, etc.).
    """
    TYPES = {
            UUID.type:UUID,
            Blob.type:Blob,
            Tree.type:Tree,
            Commit.type:Commit,
            ObjectStoreObject.type:ObjectStoreObject,
            }

    def __init__(self, backend, partition=''):
        """
        @param backend instance providing ion.data.store.IStore interface.
        @param partition Logical name spacing in an otherwise flat
        key/value space.
        @note Design decision on qualifying/naming a store name space (like
        a git repository tree)
        """
        cas.CAStore.__init__(self, backend, partition)
        self.partition = partition
        self.storemeta = cas.StoreContextWrapper(backend, partition + '.meta.')
        refs = cas.StoreContextWrapper(backend, partition + '.refs.')
        self.type = reflect.fullyQualifiedName(self.__class__)

    @classmethod
    def new(cls, backend, name):
        """
        @brief Initialize an Object Store in the backend.  
        This is a major operation, like formating a blank hard drive; In
        general, this only needs to be done once to a backend.
        @retval A Deferred that succeeds with a new instance.
        """
        inst = cls(backend, name)
        d = inst._store_exists()

        def _succeed(result):
            if not result:
                d = inst._init_store_metadata()
                return d 
            return _fail(result)

        def _fail(result):
            return defer.fail(ObjectStoreError('Partition name already exists'))

        d.addCallback(_succeed)
        d.addErrback(lambda r: _fail(r))
        return d

    @classmethod
    def load(cls, backend, name):
        """
        @brief Connect to an existing object store namespace that lives
        inthe given backend.
        @retval A Deferred that succeeds with an instance of ObjectStore
        """
        inst = cls(backend, name)
        d = inst._store_exists()

        def _succeed(result):
            if result:
                return inst
            return defer.fail(ObjectStoreError("Partition name does not exist"))

        def _fail(result):
            return defer.fail(ObjectStoreError("Error checking partition named %s" % name))

        d.addCallback(_succeed)
        d.addErrback(lambda r: _fail(r))

    @defer.inlineCallbacks
    def _init_store_metadata(self):
        """
        @brief write basic information about this store
        """
        yield self.storemeta.put('type', self.type)
        defer.returnValue(self) # Return this instance

    def _get_store_meta(self):
        d = self.storemeta.get('type')

        def _raise_if_none(res):
            if not bool(res):
                raise ObjectStoreError("Store meta not found")
            return res
        d.addCallback(_raise_if_none)
        return d

    def _store_exists(self):
        """
        @brief Verify the backend IStore contains the keys that represent
        this stores namespace.
        @retval A Deferred 
        """
        d = self._get_store_meta()
        d.addCallback(lambda res: True)
        d.addErrback(lambda res: False)
        return d

class ObjectStore(BaseObjectStore):

    @defer.inlineCallbacks
    def create(self, name, objectClass):
        """
        @param name of object store object to create...
        @param baseClass of object store object.
        @brief Create a new object named 'name'. This name should not exist
        yet in the object store.
        @retval A Deferred that succeeds with a new instance of ObjectChassis.
        """
        if not (yield self._object_exists(name)):
            yield self._create_object(name, objectClass)
            obj = yield self._build_object(name)
            defer.returnValue(obj)
        else:
            raise ObjectStoreError('Error creating %s object %s' % (objectClass.__name__, name,))

    @defer.inlineCallbacks
    def _object_class(self, objectClass):
        """

        """
        obs = objectClass().encode()
        blobs = [(name, Blob(val)) for name, val in obs]
        for n, b in blobs:
            yield self.put(b)
        childs = [Element(name, blob) for name, blob in blobs]
        tree = Tree(*childs)
        tree_id = yield self.put(tree)
        defer.returnValue(tree)

    @defer.inlineCallbacks
    def _create_object(self, name, objectClass):
        uuid_obj = UUID(name)
        id = yield self.put(uuid_obj)
        obj_class = reflect.fullyQualifiedName(objectClass)
        obj_class_obj = Blob(obj_class)
        yield self.put(obj_class_obj)
        attrs = yield self._object_class(objectClass)
        obj_tree = ObjectStoreObject(('name', uuid_obj), 
                                    ('class', obj_class_obj),
                                    ('attrs', attrs))
        obj_id = yield self.put(obj_tree)
        yield self.objs.put(name, obj_id)
        defer.returnValue(obj_id)


    @defer.inlineCallbacks
    def _build_object(self, name):
        """
        @brief General mechanical process for creating a local instance of
        an object store object.
        @note Not Using Object Store Partition Namespace Yet.
        """
        id = yield self.objs.get(name)
        obj_obj = yield self.get(id)
        yield obj_obj.load(self)
        objectClass = obj_obj['class'].content
        keyspace = cas.StoreContextWrapper(self.backend, self.partition + '.' + id + ':')
        obj = ObjectChassis(self, keyspace, objectClass)
        defer.returnValue(obj)

    @defer.inlineCallbacks
    def _object_exists(self, name):
        """
        @brief does object store object exist?
        @param name in this context is the id of the cas uuid object.
        @retval A Deferred
        """
        try:
            obj = yield self.get(cas.sha1(name))
            exists = True
        except cas.CAStoreError:
            exists = False
        defer.returnValue(exists)

    @defer.inlineCallbacks
    def clone(self, name):
        """
        @param name uuid of object store object.
        @brief Clone an object from the object store. The semantic of
        'clone' as opposed to 'get' is very important. Objects in the
        object store represent [potentially mutable] models of immutable
        constituents. 'Getting' is not the appropriate verb because you
        are not necessarily retrieving some canonical state, you are
        retrieving a distributed object with a known 'reference' name; this
        makes much sense when you consider the compliment 'put' verb. There
        is no 'put', there is 'commit', and update ref...
        """
        if (yield self._object_exists(name)):
            obj = yield self._build_object(name)
            defer.returnValue(obj)

class Identity(StoreClass):
    name = TypedAttribute(str)
    age = TypedAttribute(int)
    email = TypedAttribute(str)

@defer.inlineCallbacks
def _test(ns):
    from ion.data import store
    s = yield store.Store.create_store()
    obs = yield ObjectStore.new(s, 'test_partition')
    obj = yield obs.create('thing', Identity)
    ns.update(locals())
    """
    ind = yield obj.checkout()
    ind.name = 'Carlos S'
    ind.email = 'carlos@ooici.biz'
    yield obj.commit()
    ind = yield obj.checkout()
    ind.name = 'wwww S'
    ind.email = 'carlos@ooici.biz'
    yield obj.commit()
    ind = yield obj.checkout()
    ind.name = 'Carly S'
    ind.email = 'carlos@ooici.com'
    yield obj.commit()
    ind = yield obj.checkout()
    """
