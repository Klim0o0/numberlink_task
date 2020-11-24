class FieldSaver:

    @staticmethod
    def save(fields, path):
        with open(path, 'w', encoding='UTF-8') as file:
            for field in fields:
                file.write(str(field)+'\n\n')
