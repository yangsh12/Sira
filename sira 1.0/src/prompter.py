import re
from utils import glob_dic, func_log


class Prompter:

    blank = " "

    def __init__(self):
        self.separater = re.compile("\\s+")

    @func_log
    def auto_complete(self, position, interactive, command):
        result = []
        complete = False
        l = len(command)
        if l > 0 and command[-1] != Prompter.blank:
            complete = True
        elif l > 1 and command[-2] == Prompter.blank:
            return result

        tokens = self.separater.split(command.strip())
        for i, token in enumerate(tokens):
            pre_position = position
            # traverse every chlid nodes
            for child in position.getchildren():
                if child.tag == "keyword" and child.attrib['name'] == token:
                    position = child
                    break
                    
                elif (child.tag == "optional"
                      or child.tag == "required") and token:
                    if interactive and child.find(
                            "./keyword") is None and not complete:
                        return result
                    position = child
                    break

            if position == pre_position and l > 0:
                if ((not complete and position.find("./keyword") is None)
                        or (complete and i != len(tokens) - 1)):
                    return result

        keywords = position.findall("./keyword")
        if (not complete and keywords) or (complete
                                           and position.tag == "keyword"):
            for keyword in keywords:
                name = keyword.attrib['name']
                if complete and name.startswith(tokens[-1]):
                    result.append(name)
                elif not complete:
                    result.append(name)

        elif complete and position.tag == "cmd":
            option = position.getchildren()
            for op in option:
                name = op.attrib['name']
                if name.startswith(command):
                    result.append(name)

        else:
            option = position.find("./required") if not complete else position
            if not option:
                option = position.find("./optional")

            if option and option.attrib['name'] in glob_dic.tips.dic:
                result = glob_dic.tips.get_value(option.attrib['name'])
                if complete:
                    cl = []
                    for s in result:
                        if s.startswith(tokens[-1]):
                            cl.append(s)
                    result = cl

        return result
