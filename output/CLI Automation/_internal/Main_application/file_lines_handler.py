import logging
from tkinter import messagebox
from abc import ABC, abstractmethod
import re


class Abstract_class_file_lines_handler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def file_lines_cleaner(self):
        pass

    @abstractmethod
    def file_lines_starter_filter(self):
        pass

    @abstractmethod
    def file_lines_contains_filter(self):
        pass

    @abstractmethod
    def file_lines_pattern_filter(self):
        pass


class File_lines_handler(Abstract_class_file_lines_handler):
    def __init__(self):
        super().__init__()

    def file_lines_cleaner(self, file_lines_list: list) -> list:
        """
            Strips the lines of any character sequence and returns the clean list of lines
            
            Arguments : (file_lines_list)
                file_lines_list ===> list
                    description =====> contains the list of non-cleaned lines
                    
            return cleaned_file_list
                cleaned_file_list ===> list
                    description =====> list of file lines without any escape sequences in file lines
        """
        try:
            # logging.info(f"Got the file_lines_list => {file_lines_list}")
            if isinstance(file_lines_list, list):
                cleaned_file_list = [line.strip() for line in file_lines_list if (len(line.strip()) > 0)]

                return cleaned_file_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_starter_filter(self, file_lines_list: list, start_word: str) -> list:
        """
            Filters the lines from the given list of file lines starting from the given start word
            
            Arguments : (file_lines_list, start_word)
                file_lines_list ===> list
                    description =====> contains the list of lines from the file.
                    
                start_word ===> str
                    description =====> contains the word for which we need to filter the list with lines starting from the given start_word
                    
            return filtered_lines_list
                filtered_lines_list ===> list
                    description =====> contains the list of lines starting with the given start word
        """
        try:
            if isinstance(file_lines_list, list):
                start_word = start_word.strip()
                # compiled_pattern = re.compile(rf"^{start_word}[\s,\w]*$")
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                # print(file_lines_list)
                # print(start_word)
                # print(file_lines_list[0].startswith("Last"))
                # filtered_lines_list = [line for line in file_lines_list if (re.search(compiled_pattern, line))]
                filtered_lines_list = [line for line in file_lines_list if (line.startswith(start_word))]

                del file_lines_list
                # print(filtered_lines_list.sort())
                return sorted(filtered_lines_list)

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_contains_filter(self, file_lines_list: list, word_to_search_for: str) -> list:
        """
            Filters the lines from the given list of file lines containing the given word to search for

                Arguments : (file_lines_list, word_to_search_for)
                    file_lines_list ===> list
                        description =====> contains the list of lines from the file.

                    word_to_search_for ===> str
                        description =====> contains the word for which we need to filter the list with lines containing the given word_to_search_for

                return filtered_lines_list
                    filtered_lines_list ===> list
                        description =====> contains the list of lines starting with the given start word
        """
        try:
            if isinstance(file_lines_list, list):
                logging.info("Got the file_lines_list from the caller {}")
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                word_to_search_for = word_to_search_for.strip()

                filtered_lines_list = [line for line in file_lines_list if (line.__contains__(word_to_search_for))]

                del file_lines_list
                return sorted(filtered_lines_list)

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title= 'TypeError',
                                 message= str(e))

    def file_lines_pattern_filter(self, file_lines_list: list, pattern_to_search_for: str) -> list:
        """
            Filters the lines from the given list of file lines containing the given word to search for

                Arguments : (file_lines_list, start_word)
                    file_lines_list ===> list
                        description =====> contains the list of lines from the file.

                    pattern_to_search_for ===> str
                        description =====> contains the regex pattern for which we need to filter the list with lines containing the regex pattern

                return filtered_lines_list
                    filtered_lines_list ===> list
                        description =====> contains the list of lines starting with the given pattern
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                compiled_pattern = re.compile(pattern=pattern_to_search_for)

                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                filtered_lines_list = [line for line in file_lines_list if (re.search(pattern=compiled_pattern, string=line))]

                del file_lines_list
                return sorted(filtered_lines_list)

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_chunk_divisor(self, file_lines_list: list, start_string: str, end_string_pattern: str) -> list:
        """Gets the chunks from file_lines_list

        Args:
            file_lines_list (list): _description_ : list of file lines
            start_string (str): _description_ : first keywords from where parsing of chunk lines will be started
            end_string_pattern (str): _description_ : last string pattern till where parsing of chunk lines will be terminated
        
        return:
            filtered_lines_list (list): _description_ : chunk of parsed file lines
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                start_index = 0
                end_index = 0

                logging.info(f"Got the start string => {start_string}")
                logging.info(f"Got the end string pattern=> {end_string_pattern}")

                compiled_pattern = re.compile(end_string_pattern)

                i = 0
                while i < len(file_lines_list):
                    file_line = file_lines_list[i]

                    if file_line.startswith(start_string):
                        logging.info(f"Got the start string at {i} for start string {start_string}")
                        start_index = i

                    if re.search(compiled_pattern, file_line) is not None:
                        if (i > start_index) and (start_index > 0):
                            logging.debug(f"{start_index = }")
                            logging.info(f"found end string pattern at {i}")
                            end_index = i
                            break
                    i += 1

                filtered_lines_list = file_lines_list[start_index:end_index]

                return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))
