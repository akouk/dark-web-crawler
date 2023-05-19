class DataProcessor:
    @staticmethod
    def file_to_set(file_name):
        """Read a file and convert each line to a set."""
        results = set()
        with open(file_name, 'r') as file:
            for line in file:
                results.add(line.replace('\n', ''))
        return results

    @staticmethod
    def set_to_file(links, file_name):
        """Write each item in a set to a file as separate lines."""
        with open(file_name, 'w') as file:
            for link in sorted(links):
                file.write(link + '\n')
