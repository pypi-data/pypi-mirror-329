from antelop.utils.datajoint_utils import delete_restriction, delete_column
import re


def delete_patch(table):
    """
    This is applied on the instantiated tables to make them a subquery
    """

    # don't show deleted entries
    restriction = delete_restriction(table, "False")
    table = table & restriction
    _, projection = delete_column(table)
    table = table.proj(*projection)

    return table


def check_admin(query):
    username = query.connection.get_user().split("@")[0]
    admin = (query.tables["Experimenter"] & {"experimenter": username}).fetch1("admin")
    return admin


def safe_delete(query):
    with query.connection.transaction:
        data = (query._admin() & query.restriction).proj()
        restriction = delete_restriction(query._admin(), "True")
        for i in data:
            query._admin().update1({**i, **restriction})


def check_username(query):
    username = query.connection.get_user().split("@")[0]
    status = len(query - {"experimenter": username}) == 0
    return status


def full_names(tables):
    return {val.full_table_name: key for key, val in tables.items()}


def patch_table(table):
    """
    This is applied directly on the dj.Table objects
    """

    for method in ["insert", "delete", "update1", "delete_quick", "insert1"]:
        setattr(table, method, None)

    def help(self):
        print("Antelop table:")

        pattern = r'`[^`]+_([^`]+)`.`([^`]+)`'  # Only capture after _ and table name
        match = re.search(pattern, self.full_table_name)
        schema, table = match.groups()
        schema = schema.capitalize()
        table = ''.join([word.capitalize() for word in table.replace('#','_').split('_')])

        print(f"Schema: {schema}")
        print(f"Table: {table}")
        print("\n")

        print(self.original_heading)

        print("\n")
        print("Methods:")
        print("  - fetch()")
        print("  - fetch1()")
        print("  - delete()")
        print("  - insert()")
        print("  - insert1()")
        print("  - update1()")
        print("\n")
        

    setattr(table, "help", help)

    def delete(self, safemode=True, force=False):
        admin = check_admin(self)

        if not admin:
            if not safemode and force:
                query = self._admin() & self.restriction
                query.delete(safemode=False)
            elif not safemode:
                raise PermissionError(
                    "You do not have permission to perform permanent deletes"
                )
            elif safemode:
                safe_delete(self)

        else:
            if check_username(self):
                if safemode:
                    safe_delete(self)
                else:
                    query = self._admin() & self.restriction
                    query.delete(safemode=False)
            else:
                raise PermissionError(
                    "You do not have permission to delete entries for other users"
                )

    setattr(table, "delete", delete)

    def insert(self, *args, **kwargs):
        admin = check_admin(self)

        if not admin:
            if not check_username(self):
                raise PermissionError(
                    "You do not have permission to insert entries for other users"
                )
            else:
                self._admin().insert(*args, **kwargs)
        else:
            self._admin().insert(*args, **kwargs)

    setattr(table, "insert", insert)

    def insert1(self, *args, **kwargs):
        admin = check_admin(self)

        if not admin:
            if not check_username(self):
                raise PermissionError(
                    "You do not have permission to insert entries for other users"
                )
            else:
                self._admin().insert1(*args, **kwargs)
        else:
            self._admin().insert1(*args, **kwargs)

    setattr(table, "insert1", insert1)

    def update1(self, *args, **kwargs):
        admin = check_admin(self)

        if not admin:
            if not check_username(self):
                raise PermissionError(
                    "You do not have permission to update entries for other users"
                )
            else:
                self._admin().update1(*args, **kwargs)
        else:
            self._admin().update1(*args, **kwargs)

    setattr(table, "update1", update1)

    return table


def full_restore(query):
    """
    Function performs a full restore on the deleted objects and all its deleted children
    Since tables can have multiple parents, it needs to additionally check there are no remaining
    deleted parents
    """

    update_dict = {}

    with query.connection.transaction:
        # what to update
        for tablename in query.descendants():
            table = query.tables[full_names(query.tables)[tablename]]
            child_query = table & query.proj() & delete_restriction(table, "True")
            for parentname in table.parents():
                if parentname not in query.tables:
                    parent = query.tables[full_names(query.tables)[parentname]]
                    col, _ = delete_column(parent)
                    child_query = child_query & (
                        parent.proj(*col) & delete_restriction(parent, "False")
                    )
            update_dict[tablename] = child_query.proj().fetch(as_dict=True)

        # update
        for tablename, data in update_dict.items():
            for i in data:
                deleted = delete_restriction(
                    query.tables[full_names(query.tables)[tablename]], "False"
                )
                query.tables[full_names(query.tables)[tablename]].update1(
                    {**i, **deleted}
                )


def patch_admin(table):
    """
    We also add restore functionality to the admin tables
    """

    def restore(self):
        """
        Applied on the admin table query object
        """

        admin = check_admin(self)

        if not admin:
            raise PermissionError("You do not have permission to restore entries")

        else:
            print("Restoring data")
            full_restore(self)

    setattr(table, "restore", restore)

    return table
