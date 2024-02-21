#!/usr/bin/python3
""" Console Module """

import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes

    prompt = "(hbnb) "
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def strip_line(self, line):
        """strips the argument and return a string of command"""
        lists = []
        lists.append(args[0])
        try:
            my_dict = eval(
                line[1][line[1].find('{'):line[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = line[1][line[1].find('(')+1:line[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default_arg(self, args):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        lists = args.split('.')
        if len(lists) >= 2:
            if lists[1] == "all()":
                self.do_all(lists[0])
            elif lists[1] == "count()":
                self.count(lists[0])
            elif lists[1][:4] == "show":
                self.do_show(self.strip_line(lists))
            elif lists[1][:7] == "destroy":
                self.do_destroy(self.strip_line(lists))
            elif lists[1][:6] == "update":
                cmd_args = self.strip_line(lists)
                if isinstance(cmd_args, list):
                    obj = storage.all()
                    key = cmd_args[0] + ' ' + cmd_args[1]
                    for key, value in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(key, value))
                else:
                    self.do_update(cmd_args)
        else:
            cmd.Cmd.default_args(self, args)

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        """if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        """
        try:
            lists = args.split(" ")

            kwargs = {}
            for i in range(1, len(lists)):
                key, value = tuple(lists[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                created_obj = eval(lists[0])()
            else:
                created_obj = eval(lists[0])(**kwargs)
                storage.new(created_obj)
            print(created_obj)
            created_obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        try:
            if not args:
                raise SyntaxError()
            lists = args.split(" ")
            if lists[0] not in self.classes:
                raise NameError()
            if len(lists) < 2:
                raise IndexError()
            objs = storage.all()
            key_args = lists[0] + '.' + lists[1]
            if key_args in objects:
                del objs[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        if not args:
            objs = storage.all()
            print([objs[key].__str__() for key in objs])
            return
        try:
            cmd_args = args.split(" ")
            if cmd_args[0] not in self.classes:
                raise NameError()

            objs = storage.all(eval(cmd_args[0]))
            print([objs[key].__str__() for key in objs])

        except NameError:
            print("** class doesn't exist **")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """

        try:
            if not args:
                raise SyntaxError()
            lists = split(args, " ")
            if lists[0] not in self.classes:
                raise NameError()
            if len(lists) < 2:
                raise IndexError()
            objs = storage.all()
            key = lists[0] + '.' + lists[1]
            if key not in objs:
                raise KeyError()
            if len(lists) < 3:
                raise AttributeError()
            if len(lists) < 4:
                raise ValueError()
            value = objs[key]
            try:
                value.__dict__[lists[2]] = eval(lists[3])
            except Exception:
                value.__dict__[lists[2]] = lists[3]
                value.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
