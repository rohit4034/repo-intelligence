class PythonASTExtractor:

    def extract(self, root, source, data):

        # walk through all nodes recursively
        self._walk(root, source, data)


    def _walk(self, node, source, data):

        if node.type == "import_statement":
            data["imports"].append(self._parse_import(node, source))

        elif node.type == "import_from_statement":
            data["imports"].append(self._parse_import(node, source))

        elif node.type == "function_definition":
            data["functions"].append(self._parse_function(node, source))

        elif node.type == "class_definition":
            cls = self._parse_class(node, source)

            data["classes"].append(cls)

            for m in cls["methods"]:
                data["methods"].append(m)

        elif node.type == "call":
            call = self._parse_call(node, source)
            if call:
                data["calls"].append(call)

        # recurse through children
        for child in node.children:
            self._walk(child, source, data)


    def _parse_function(self, node, source):

        name_node = node.child_by_field_name("name")

        code = source[node.start_byte:node.end_byte].decode()

        return {
            "name": self._text(name_node, source),
            "line_start": node.start_point[0] + 1,
            "line_end": node.end_point[0] + 1,
            "code": code
        }


    def _parse_class(self, node, source):

        name_node = node.child_by_field_name("name")
        class_name = self._text(name_node, source)

        class_code = source[node.start_byte:node.end_byte].decode()

        methods = []

        for child in node.children:

            if child.type == "block":

                for c in child.children:

                    if c.type == "function_definition":

                        method_name = self._text(
                            c.child_by_field_name("name"),
                            source
                        )

                        method_code = source[
                            c.start_byte:c.end_byte
                        ].decode()

                        methods.append({
                            "class": class_name,
                            "name": method_name,
                            "line_start": c.start_point[0] + 1,
                            "line_end": c.end_point[0] + 1,
                            "code": method_code
                        })

        return {
            "name": class_name,
            "line_start": node.start_point[0] + 1,
            "line_end": node.end_point[0] + 1,
            "code": class_code,
            "methods": methods
        }


    def _parse_import(self, node, source):

        return {
            "import": source[node.start_byte:node.end_byte].decode()
        }


    def _parse_call(self, node, source):

        func_node = node.child_by_field_name("function")

        if not func_node:
            return None

        call_name = source[
            func_node.start_byte:func_node.end_byte
        ].decode()

        return {
            "call": call_name,
            "line": node.start_point[0] + 1
        }


    def _text(self, node, source):

        return source[node.start_byte:node.end_byte].decode()