from abc import ABC,abstractmethod
import re

class Abstract_class_file_lines_handler(ABC):
    def __init__():
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
        pass
    
    def file_lines_cleaner(self,file_lines_list : list) -> list:
        """
            Strips the lines of any character sequence and returns the clean list of lines
            
            Arguments : (file_lines_list)
                file_lines_list ===> list
                    description =====> contains the list of non-cleaned lines
                    
            return cleaned_file_list
                cleaned_file_list ===> list
                    description =====> list of file lines without any escape sequences in file lines
        """
        cleaned_file_list = [line for line in file_lines_list if(len(line.strip() > 0))]
        del file_lines_list
        
        return cleaned_file_list
    
    def file_lines_starter_filter(self,file_lines_list : list, start_word : str) -> list:
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
        
        file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
        
        start_word = start_word.strip()
        filtered_lines_list = [line for line in file_lines_list if line.startswith(start_word)]
        
        del file_lines_list
        return result_list
    
    def file_lines_contains_filter(self, file_lines_list: list, word_to_search_for : str) -> list:
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
        
        file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
        
        word_to_search_for = word_to_search_for.strip()
        
        filtered_lines_list = [line for line in file_lines_list if(line.__contains__(word_to_search_for))]
        
        del file_lines_list
        return filtered_lines_list

    def file_lines_pattern_filter(self,file_lines_list: list, pattern_to_search_for: str) -> list:
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
        compiled_pattern = re.compile(pattern=pattern_to_search_for)
        
        file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
        
        filtered_lines_list = [line for line in file_lines_list if(re.search(pattern=compiled_pattern,string=line))]
        
        del file_lines_list
        return filtered_lines_list