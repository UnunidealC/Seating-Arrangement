class Attribute(object):
    """class Attribute inherit from class object"""

    # initializer for class Attribute
    def __init__(self, lst):
        self._attr_name = lst[1]
        self._attr_type = lst[2]
        self._constraint = lst[3]
        self._primary_key = lst[4]
        self._foreign_key = lst[5]

    # Mutator Functions
    def set_attr_name(self, new_attr_name):
        self._attr_name = new_attr_name

    def set_attr_type(self, new_attr_type):
        self._attr_type = new_attr_type

    def set_constraint(self, new_constraint):
        self._constraint = new_constraint

    def set_primary_key(self, new_primary_key):
        self._primary_key = new_primary_key

    def set_foreign_key(self, new_foreign_key):
        self._foreign_key = new_foreign_key

    # Accessor Functions
    def get_attr_name(self):
        return self._attr_name

    def get_attr_type(self):
        return self._attr_type

    def get_constraint(self):
        return self._constraint

    def get_primary_key(self):
        return self._primary_key

    def get_foreign_key(self):
        return self._foreign_key

    # String Representation of Class Attribute
    def __str__(self):
        result = ""

        result += "{self._attr_name} {self._attr_type} {self._constraint}".format(self=self)

        return result

    def get_self_str(self):
        if self._attr_type != "Integer" and self._attr_type != "Float":
            return "'{{self._{}}}'".format(self._attr_name)
        else:
            return "{{self._{}}}".format(self._attr_name)

    def get_equal_str(self):
        return "{} = {}".format(self._attr_name, self.get_self_str())


class SQLiteClass(object):
    def __init__(self, class_name, attr_list):
        self._class_name = class_name
        self._attr_list = attr_list

        self._tab = " " * 4

    def get_attr_list(self):
        return self._attr_list

    def add_attr(self, new_attr):
        self._attr_list.append(new_attr)

    def generate_tuple_string(self, attr_list, operation):
        result = ""
        for element in attr_list:
            if operation == "attr_name":
                result += element.get_attr_name() + ", "
            elif operation == "self_str":
                result += element.get_self_str() + ", "
            elif operation == "equal_str":
                result += element.get_equal_str() + ", "
            else:
                print("Error! Wrong type operation")
        if result[-2] == ",":
            result = result[0:-2]
        return result

    def generate_line(self, num_of_tabs, content):
        return "{}{}\n".format(self._tab*num_of_tabs, content)

    def generate_sql_line(self, content):
        return "result += \"{}\\n\"".format(content)

    def __str__(self):
        result = ""

        # 01 class definition
        result += self.generate_line(0, "class {self._class_name}(object):".format(self=self))
        result += self.generate_line(1, "\"\"\"SQLite OOP class {self._class_name}\"\"\"\n".format(self=self))

        # 02 init method
        result += self.generate_line(1, "# initializer for class{self._class_name}".format(self=self))
        # init first line
        param_list = self.generate_tuple_string(self._attr_list, "attr_name")
        result += self.generate_line(1, "def __init__(self, {}):".format(param_list, self=self))

        # init attribute assignment
        for attr in self._attr_list:
            result += self.generate_line(2, "self._{0} = {0}".format(attr.get_attr_name()))

        result += "\n"

        # 03 Mutators
        result += self.generate_line(1, "# Mutator Functions")

        for attr in self._attr_list:
            # setter first line
            result += self.generate_line(1, "def set_{0}(self, new_{0}):".format(attr.get_attr_name()))

            # setter content
            result += self.generate_line(2, "self._{0} = new_{0}\n".format(attr.get_attr_name()))

        # 04 Accessors
        result += self.generate_line(1, "# Accessor Functions")
        for attr in self._attr_list:
            # getter first line
            result += self.generate_line(1, "def get_{}(self):".format(attr.get_attr_name()))

            # getter content
            result += self.generate_line(2, "return self._{}\n".format(attr.get_attr_name()))

        # 05 to string function
        result += self.generate_line(1, "# String Representation of Class {self._class_name}".format(self=self))
        result += self.generate_line(1, "def __str__(self):")
        result += self.generate_line(2, "result = \"\"\n".format(self=self))
        result += self.generate_line(2, "return result\n".format(self=self))

        # SQLite special attr list
        pk_attr_list = list(filter(lambda attr: attr.get_primary_key() == "Yes", self._attr_list))
        fk_attr_list = list(filter(lambda attr: attr.get_foreign_key(), self._attr_list))

        # 06 SQLite: static method: create table function
        result += self.generate_line(1, "# SQLite: Create Table of Class {self._class_name}".format(self=self))
        result += self.generate_line(1, "@staticmethod")
        result += self.generate_line(1, "def create_table():")
        result += self.generate_line(2, "result = \"\"")

        # create table first line
        result += self.generate_line(2, self.generate_sql_line("CREATE TABLE {self._class_name}(".format(self=self)))

        # attribute, type and constraints
        for attr in self._attr_list:
            result += self.generate_line(2, self.generate_sql_line("{},".format(str(attr))))

        # primary key
        primary_key_tuple = self.generate_tuple_string(pk_attr_list, "attr_name")
        result += self.generate_line(2, self.generate_sql_line("PRIMARY KEY({}),".format(primary_key_tuple)))

        # foreign key
        for attr in fk_attr_list:
            result += self.generate_line(2, self.generate_sql_line(
                "FOREIGN KEY ({}) REFERENCES {},".format(attr.get_attr_name(), attr.get_foreign_key(), self=self)))

        # close and return
        result = result[0:-5] + result[-4:] # remove last comma
        result += self.generate_line(2, self.generate_sql_line(")"))
        result += self.generate_line(2, "return result\n")

        # 07 SQLite: create new record
        result += self.generate_line(1, "# SQLite: Create new record")
        result += self.generate_line(1, "def create_new_record(self):")
        result += self.generate_line(2, "result = \"\"")

        # Insert statement 1st line
        result += self.generate_line(2, self.generate_sql_line("INSERT INTO {self._class_name}".format(self=self)))

        # Insert statment 2nd line
        attr_str = self.generate_tuple_string(self._attr_list, "attr_name")
        result += self.generate_line(2, self.generate_sql_line("({})".format(attr_str)))

        # Insert statment 3rd line
        result += self.generate_line(2, self.generate_sql_line("VALUES"))

        # Insert statement 4th line
        attr_str = self.generate_tuple_string(self._attr_list, "self_str")
        result += self.generate_line(2, self.generate_sql_line("({})".format(attr_str))+".format(self=self)")

        # Return
        result += self.generate_line(2, "return result\n")

        # 08 SQLite: update record based on primary key
        result += self.generate_line(1, "# SQLite: Update record based on primary key")
        result += self.generate_line(1, "def update_record(self):")
        result += self.generate_line(2, "result = \"\"")

        # Update statement 1st line
        result += self.generate_line(2, "result += \"UPDATE {self._class_name} SET\\n\"".format(self=self))

        # Update statment 2nd line
        attr_str = self.generate_tuple_string(self._attr_list, "equal_str")
        result += self.generate_line(2, self.generate_sql_line(attr_str)+".format(self=self)")

        # Update statment 3rd line
        result += self.generate_line(2, self.generate_sql_line("WHERE"))

        # Update statement 4th line
        attr_str = self.generate_tuple_string(pk_attr_list, "equal_str")
        result += self.generate_line(2, self.generate_sql_line(attr_str)+".format(self=self)")

        # Return
        result += self.generate_line(2, "return result\n")

        # 09 SQLite: delete record based on primary key
        result += self.generate_line(1, "# SQLite: Delete record based on primary key")
        result += self.generate_line(1, "def delete_record(self):")
        result += self.generate_line(2, "result = \"\"")

        # Delete statement 1st line
        result += self.generate_line(2, "result += \"DELETE FROM {self._class_name} WHERE\\n\"".format(self=self))

        # Delete statement 2th line
        attr_str = self.generate_tuple_string(pk_attr_list, "equal_str").replace(",", " and")
        result += self.generate_line(2, self.generate_sql_line(attr_str) + ".format(self=self)")

        # Return
        result += self.generate_line(2, "return result\n")

        return result


class SQLiteClassGenerator(object):
    def __init__(self):
        self._class_list = []

    def read_file(self, file_name):
        f = open(file_name, "r")
        raw_data = f.read()
        f.close()

        non_empty_rows = list(filter(lambda r: r != "", raw_data.split("\n")))
        row_list = list(map(lambda r: r.split(";"), non_empty_rows))[1:]

        sc_list = []

        for row in row_list:
            if row[0]:
                sc = SQLiteClass(row[0], [])
                sc_list.append(sc)
            attr = Attribute(row)
            sc.add_attr(attr)

        for sc in sc_list:
            self._class_list.append(sc)

    def generate(self):
        f = open("SQLiteOOP.py", "w")
        content = ""

        for sc in self._class_list:
            content += str(sc) + "\n"

        f.write(content)
        f.close()

pcg = SQLiteClassGenerator()
pcg.read_file("new_class.csv")
pcg.generate()