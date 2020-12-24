class DazCmsRouter:
    def db_for_write(self, model, **hints):
        if model._meta.app_label == "dazcms":
            return "dazcms"
        return None

    def db_for_read(self, model, **hints):
        return self.db_for_write(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "dazcms":
            return False
        return None
