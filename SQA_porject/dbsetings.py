class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    defaultDB = 'default'
    app_label_list = ['auth', 'authtoken', 'authprofile','admin']


    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in self.app_label_list:
            return self.defaultDB
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in self.app_label_list:
            return self.defaultDB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in self.app_label_list or \
           obj2._meta.app_label in self.app_label_list:
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == self.defaultDB:
            return model._meta.app_label in self.app_label_list
        elif model._meta.app_label in self.app_label_list:
            return False
        return None


class MasterSlaveRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen slave.
        """
        return 'mariadb'

    def db_for_write(self, model, **hints):
        """
        Writes always go to master.
        """
        return 'mariadb'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        db_list = ('mariadb',)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True