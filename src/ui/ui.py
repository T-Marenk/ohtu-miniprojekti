from ui.reference_reader import ReferenceReader
from services.reference_service import ReferenceType

class UI:
    def __init__(self, app):
        self.app = app
        self.reference_reader = ReferenceReader()

    def run(self):
        while True:
            self.print_instructions()

            options = {
                "1": self.create_file, "2": self.view_ref,
                "3": self.add_ref, "4": self.del_ref
            }

            option = input()

            if option in options:
                options[option]()
            elif option == "5":
                break

    def create_file(self):
        filename = input("\nMinkä nimisen tiedoston haluat luoda? ")

        data = self.app.get_all_references()

        try:
            self.app.create_bibtex_file(data, filename)
            print("Tiedosto luotu projektin juurihakemistoon!")
        except ValueError as error:
            print(error, "\n")

    def print_instructions(self):
        instructions = ["Luoda tiedosto, paina 1",
                        "Tarkastella luotuja viitteitä, paina 2",
                        "Lisää uusi viite, paina 3",
                        "Poista viite, paina 4",
                        "Sulje ohjelma, paina 5"]

        print("\n-----------")
        print(self.text_to_bold("Mitä haluat tehdä?"))
        for instruction in instructions:
            print("\n" + instruction)

    def sort_data(self, data, sorting_key, order):
        if sorting_key == "1":
            if order == "1":
                data.sort(key=lambda ref: ref.year, reverse=False)
            if order == "2":
                data.sort(key=lambda ref: ref.year, reverse=True)

        elif sorting_key == "2":
            if order == "2":
                data.reverse()
        return data

    def view_ref(self):
        tag_set = self.app.get_tags()
        tag = input(
            f"Haluatko suodattaa listaa tagin perusteella? Syötä tagi tai jätä tyhjäksi. \n Tagit: {tag_set} ")
        sorting_key = input(
            "\nMillä perusteella haluat järjestää listan? \nVuosiluvun perusteella, paina 1 \nLisäysjärjestyksessä, paina 2 \n")
        order = input(
            "\nHaluatko listan \nNousevassa järjestyksessä, paina 1 \nLaskevassa järjestyksessä, paina 2 \n")

        if tag == "":
            refs = self.app.get_all_references()
        else:
            refs = self.app.filter_by_tag(tag)
        book_data = refs["book_references"]
        web_data = refs["web_references"]
        book_data_sorted = self.sort_data(book_data, sorting_key, order)
        web_data_sorted = self.sort_data(web_data, sorting_key, order)

        title_bar1 = f'{self.text_to_bold("Author")}                    {self.text_to_bold("Title")}                                         {self.text_to_bold("Year")} {self.text_to_bold("Publisher")}                 {self.text_to_bold("Key")}    {self.text_to_bold("Tagi")}'
        title_bar2 = "------------------------- --------------------------------------------- ---- ------------------------- -----------"

        print(self.text_to_bold(f"Kirjaviitteet:\n{title_bar1}\n{title_bar2}"))

        for ref in book_data_sorted:
            self.print_book_ref(ref)

        title_bar1 = f'{self.text_to_bold("Author")}                    {self.text_to_bold("Title")}                                         {self.text_to_bold("Year")} {self.text_to_bold("URL")}                       {self.text_to_bold("Key")}'
        title_bar2 = "------------------------- --------------------------------------------- ---- ------------------------- -----------"

        print(self.text_to_bold(f"Verkkosivuviitteet:\n{title_bar1}\n{title_bar2}"))

        for ref in web_data_sorted:
            self.print_web_ref(ref)

    def add_ref(self):
        answer = input(
            "Haluatko tallentaa kirjaviitteen (paina 1) vai verkkosivuviitteen (paina 2): ")
        if answer == "1":
            ref_list = self.reference_reader.book_ref_reader()
            key = ref_list[4]
            if self.app.key_used(key):
                print("Valitsemasi avain on jo käytössä")
            else:
                self.app.add_reference(ref_list, ReferenceType.Book)
        elif answer == "2":
            ref_list = self.reference_reader.web_ref_reader()
            key = ref_list[4]
            if self.app.key_used(key):
                print("Valitsemasi avain on jo käytössä")
            else:
                self.app.add_reference(ref_list, ReferenceType.Website)

    def del_ref(self):
        key = input("\nAnna avain:")

        print(self._get_ref_to_delete(key))

        answer = input("Haluatko varmasti poistaa viitteen?(kyllä k/en e)\n")

        if answer == "k":
            result = self.app.delete_reference(key)
            if result:
                print("Viitteen poisto onnistui")
            else:
                print("Viitteen poisto ei onnistunut")

    def _get_ref_to_delete(self, key):
        refs = self.app.get_all_references()
        data = refs["book_references"] + refs["web_references"]

        for ref in data:
            if key == ref.bib_key:
                return str(ref)

    def text_to_bold(self, text):
        return "\033[1m" + text + "\033[0m"

    def print_book_ref(self, ref):
        author = ref.author
        title = ref.title
        publisher = ref.publisher
        bib_key = ref.bib_key

        if len(author) > 25:
            author = author[:22] + "..."
        if len(title) > 45:
            title = title[:42] + "..."
        if len(publisher) > 25:
            publisher = publisher[:22] + "..."
        if len(bib_key) > 8:
            bib_key = bib_key[:8] + "..."

        print(f"{author:25} {title:45} {ref.year:4} {publisher:25} {bib_key:11}\n")

    def print_web_ref(self, ref):
        author = ref.author
        title = ref.title
        url = ref.url
        bib_key = ref.bib_key

        if len(author) > 25:
            author = author[:22] + "..."
        if len(title) > 45:
            title = title[:42] + "..."
        if len(url) > 25:
            url = url[:22] + "..."
        if len(bib_key) > 8:
            bib_key = bib_key[:8] + "..."

        print(f"{author:25} {title:45} {ref.year:4} {url:25} {bib_key:11}\n")
