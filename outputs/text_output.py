def save_to_text(data, filename="output.txt"):
    with open(filename, "w") as file:
        for record in data:
            file.write(f"ID: {record[0]}\n")
            file.write(f"Question: {record[1]}\n")
            file.write(f"Answer: {record[2]}\n")
            file.write(f"Model Used: {record[3]}\n")
            file.write(f"Timestamp: {record[4]}\n")
            file.write("\n" + "-"*20 + "\n")

    return filename
