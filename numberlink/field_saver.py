class FieldSaver:

    @staticmethod
    def save(field, path):
        with open(path, 'w') as file:
            for i in field.field:
                for j in i:
                    file.write(str(j))
                file.write('\n')
