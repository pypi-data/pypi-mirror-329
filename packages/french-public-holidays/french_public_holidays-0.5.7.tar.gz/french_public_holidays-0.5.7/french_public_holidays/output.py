import csv
import datetime
import json
import os
import yaml

class Output:
    """
    The Output class is responsible for saving data to files in various formats (CSV, JSON, YAML).
    It supports saving data with formatted dates and descriptions.

    Attributes:
        header (list): The header row for CSV files.
        output (str): The output file path.
        extension (str): The file extension derived from the output file path.

    Methods:
        __init__(header, output):
            Initializes the Output class with the provided header and output file path.
        save(data):
            Saves the provided data to a file based on the specified file extension.
            Supported file extensions: csv, json, yaml, yml.
        save_csv(data):
            Saves the provided data to a CSV file with formatted dates.
        save_json(data):
            Saves the provided data to a JSON file with formatted dates.
        save_yaml(data):
            Saves the provided data to a YAML file with formatted dates.
    """
    def __init__(self, header, output):
        self.header = header
        self.output = output
        self.extension = os.path.splitext(output)[1][1:] or None

    def save(self, data):
        """
        Save the provided data to a file based on the specified file extension.

        Args:
            data (dict): The data to be saved.

        Raises:
            ValueError: If the file extension is not supported.

        Supported file extensions:
            - csv: Saves data in CSV format.
            - json: Saves data in JSON format.
            - yaml: Saves data in YAML format.
            - yml: Saves data in YAML format.
        """
        if self.extension == "csv":
            self.save_csv(data)
        elif self.extension == "json":
            self.save_json(data)
        elif self.extension == "yaml":
            self.save_yaml(data)
        elif self.extension == "yml":
            self.save_yaml(data)
        else:
            raise ValueError("Extension not supported")

    def save_csv(self, data):
        """
        Save the provided data to a CSV file.

        Args:
            data (list): A list of dictionaries where each dictionary represents
                                 a set of key-value pairs to be written to the CSV file.

        Writes:
            A CSV file at the location specified by self.output. The file will contain
            a header row followed by rows of data. Dates in the data will be formatted
            as 'dd/mm/yy'.
        """
        with open(self.output, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(self.header)
            for jf in data:
                for j in jf:
                    date = datetime.datetime.strptime(j, '%Y-%m-%d').strftime('%d/%m/%y')
                    writer.writerow([date, jf[j]])

    def save_json(self, data):
        """
        Save the provided data to a JSON file with formatted dates.

        Args:
            data (list): A list of dictionaries where each dictionary represents a public holiday.
                 Each dictionary should have a date string in the format '%Y-%m-%d' as the key
                 and a description as the value.

        The method processes each dictionary in the list, converts the date string to the format '%d/%m/%y',
        and writes the resulting list of dictionaries to a JSON file specified by self.output.

        Writes:
            A JSON file at the location specified by self.output. The file will contain a list of dictionaries
            where each dictionary has a 'date' key with the date formatted as 'dd/mm/yy' and a 'description' key
            with the description of the public holiday.
        """
        with_headers = []
        for jf in data:
            for j in jf:
                with_headers.append({"date": datetime.datetime.strptime(j, '%Y-%m-%d').strftime('%d/%m/%y'), "description": jf[j]})
        with open(self.output, 'w', encoding='utf-8') as jsonfile:
            json.dump(with_headers, jsonfile, indent=4)

    def save_yaml(self, data):
        """
        Save the provided data to a YAML file with formatted dates and descriptions.

        Args:
            data (list): A list of dictionaries where each dictionary contains a date string
                         in the format '%Y-%m-%d' as the key and a description as the value.

        Writes:
            A YAML file at the location specified by self.output. The file will contain a list of dictionaries
            where each dictionary has a 'date' key with the date formatted as 'dd/mm/yy' and a 'description' key
            with the description of the public holiday.
        """
        with_headers = []
        for jf in data:
            for j in jf:
                with_headers.append({"date": datetime.datetime.strptime(j, '%Y-%m-%d').strftime('%d/%m/%y'), "description": jf[j]})
        with open(self.output, 'w', encoding='utf-8') as yamlfile:
            yaml.dump(with_headers, yamlfile, default_flow_style=False)