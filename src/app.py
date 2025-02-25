class App:
    def __init__(self, connection, reference_service, db, bibtex_generator):
        self.connection = connection
        self.reference_service = reference_service
        self.db = db
        self.bibtex_generator = bibtex_generator

    def add_reference(self, ref_list, ref_type):
        self.reference_service.add_reference(ref_list, ref_type)

    def get_all_references(self):
        return self.reference_service.get_all_references()

    def create_bibtex_file(self, data, filename):
        self.bibtex_generator.create_bibtex_file(data, filename)

    def delete_reference(self, key):
        self.reference_service.delete_reference(key)

    def key_used(self, key) -> bool:
        return self.reference_service.key_used(key)

    def filter_by_tag(self, tag):
        return self.reference_service.get_references_by_tag(tag)

    def get_tags(self):
        return self.reference_service.get_tags()
