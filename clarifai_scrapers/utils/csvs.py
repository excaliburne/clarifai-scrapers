# SYSTEM 
import csv


def write(
    headers: list, 
    data: list,
    output_file_path: str
    ) -> None:
    """
    Writes data to csv file locally

    Args:
        headers (list)
        data (list): List of dictionaries referencing the headers with keys
        output_file_path (str)
    """
    with open(output_file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)