from numberlink.field import Field


class FieldBuilder:

    @staticmethod
    def build_field_from_file(file_path):
        field = []
        with open(file_path) as file:
            for line in file:
                field_line = []
                for c in line:
                    if c != '\n':
                        field_line.append(int(c))
                field.append(field_line)
        return Field(field)
