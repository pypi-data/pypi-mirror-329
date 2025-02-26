import copy
import json

from insight_plugin.features.create.help.constants import TableHeaders
from insight_plugin.features.common.plugin_spec_util import PluginSpecConstants
from mdutils.mdutils import MdUtils


class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):  # pylint: disable=arguments-renamed
        json_string = super().encode(obj)
        return json_string.replace("true", "True").replace("false", "False")


class HelpUtil:
    @staticmethod
    def get_article(key: str):
        if key[-1] == "s":
            return "any"
        elif "aeiou".find(key[0]) != -1:
            return "an"
        else:
            return "a"

    @staticmethod
    def shallow_sort(dic: dict) -> dict:
        """
        Shallow sort a dict
        :param dic: to sort
        :return: sorted dictionary
        """
        section_spec_keys = sorted(dic)
        sorted_dict = {}
        for key in section_spec_keys:
            sorted_dict[key] = dic[key]
        return sorted_dict

    @staticmethod
    def get_new_table_text(spec: dict, table_type: [str]) -> [str]:
        """
        This method creates this list of strings that mdutils library takes for each table
        :param table_type: headers for this type of table
        :param spec: input or output block of spec
        :return: list of strings for markdown table text
        """
        starting_list = copy.copy(table_type)
        spec = HelpUtil.shallow_sort(spec)
        for key, item in spec.items():
            if table_type == TableHeaders.INPUT_HEADERS:
                next_row = [
                    key,
                    item.get(PluginSpecConstants.TYPE, "None"),
                    item.get(PluginSpecConstants.DEFAULT, "None"),
                    item.get(PluginSpecConstants.REQUIRED, "None"),
                    item.get(PluginSpecConstants.DESCRIPTION, "None"),
                    item.get(PluginSpecConstants.ENUM, "None"),
                    item.get(PluginSpecConstants.EXAMPLE, "None"),
                    item.get(PluginSpecConstants.PLACEHOLDER, "None"),
                    item.get(PluginSpecConstants.TOOLTIP, "None"),
                ]
            elif table_type == TableHeaders.OUTPUT_HEADERS:
                next_row = [
                    key,
                    item.get(PluginSpecConstants.TYPE, "None"),
                    item.get(PluginSpecConstants.REQUIRED, "None"),
                    item.get(PluginSpecConstants.DESCRIPTION, "None"),
                    item.get(PluginSpecConstants.EXAMPLE, "None"),
                ]
            elif table_type == TableHeaders.CUSTOM_TYPE_HEADERS:
                next_row = [
                    item.get(PluginSpecConstants.TITLE, key),
                    item.get(PluginSpecConstants.TYPE, "None"),
                    item.get(PluginSpecConstants.DEFAULT, "None"),
                    item.get(PluginSpecConstants.REQUIRED, "None"),
                    item.get(PluginSpecConstants.DESCRIPTION, "None"),
                    item.get(PluginSpecConstants.EXAMPLE, "None"),
                ]
            else:
                continue

            for index, value in enumerate(next_row):
                if isinstance(value, list):
                    # The CustomJSONEncoder class will convert all booleans back to what they were, prior to json.dumps (True and False stays True and False)
                    next_row[index] = json.dumps(value, cls=CustomJSONEncoder)
            starting_list.extend(next_row)

        return starting_list

    @staticmethod
    def change_title_to_description(md_file: MdUtils) -> MdUtils:
        """
        This function changes the title in the md file to ensure a similar format is maintained
        in comparison with currently existing help md's.
        :param md_file: The markdown object/file to modify.
        :return: Md_file with key title having new value of '# Description'
        """
        md_file.__dict__["title"] = (
            "# " + PluginSpecConstants.DESCRIPTION.capitalize() + "\n"
        )
        return md_file

    @staticmethod
    def make_header(markdown_obj: MdUtils, level: int, title: str):
        """
        Function to create headers that match the format of the old icon-plugin.
        Ensures document headers are a similar format to those that already exist.
        :param markdown_obj: The markdown file.
        :param level: Level of the header. 1 = #, 3, = ### etc.
        :param title: The text to be inserted into the header.
        :return: Return a header with a newline above.
        """
        markdown_obj.write("\n")
        markdown_obj.new_header(level=level, title=title)
        return markdown_obj
