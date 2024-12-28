import random
import csv
import sys


def generate_samples(n):
    #Generate sample numbers in the form "100-n" where n is the number of samples
    return[f"100-{i+1}" for i in range(n)]


def generate_csv(samples, matrix, filename="sample_data.csv"):
    #Write samples and matrix to csv file

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sample Number", "Matrix", "Conductivity"]) #Headers
        for sample, cond in samples:
            writer.writerow([sample, matrix, f"{cond:.2f} μS/cm"]) #write sample and matrix to each row


def generate_tss(input_filename="sample_data.csv", output_filename="tss_data.csv"):
    with open(input_filename, mode="r", newline="") as file_in:
        reader = csv.reader(file_in)
        next(reader) #skips headers in csv file

        #read and convert conductivity values
        tss_data = []
        for row in reader:
            sample_number = row[0]
            matrix = row[1]
            cond = float(row[2].split()[0]) #removes unit from conductivity value
            tss = cond * 0.64 #TSS formula

            tss_data.append([sample_number, matrix.upper(), f"{cond:.2f} μS/cm", f"{tss:.2f} ppm"])

    with open(output_filename, mode="w", newline="") as file_out:
        writer = csv.writer(file_out)
        writer.writerow(["Sample Number", "Matrix", "Conductivity", "T. Soluble Salts"])
        writer.writerows(tss_data)


def generate_resist(input_filename="sample_data.csv", output_filename="res_data.csv"):
    with open(input_filename, mode="r", newline="") as file_in:
        reader = csv.reader(file_in)
        next(reader)

        res_data = []
        for row in reader:
            sample_number = row[0]
            matrix = row[1]
            cond = float(row[2].split()[0])

            if matrix == "AQ":
                res = (1/cond) * 1000000 #Aqueous Resistivity formula
            elif matrix == "SD":
                res = (1/(10*cond)) * 1000000 #Solid Resistivity formula
            else:
                continue

            res_data.append([sample_number, matrix.upper(), f"{cond:.2f} μS/cm", f"{res:.2f} Ωm"])


        with open(output_filename, mode="w", newline="") as file_out:
            writer = csv.writer(file_out)
            writer.writerow(["Sample Number", "Matrix", "Conductivity", "Resistivity"])
            writer.writerows(res_data)


def main():
    while True:
        read_or_write: str = str(input("Generate a new file?  Or read existing file? (Enter 'new' or 'read'): ")).lower()
        if read_or_write in ["new", "read"]:
            break
        else:
            print("Invalid input.  Enter 'new' to create a new file or 'read' to read an existing file")

    if read_or_write == "new": #Generate samples and a new file
        while True:
            try:
                n: int = int(input("How many samples? "))
                if n > 0:
                    break
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input.  Please enter a positive integer.")

        while True:
            matrix: str = input("What is the sample matrix? (AQ or SD) ").lower()
            if matrix in ["aq", "sd"]:
                matrix = matrix.upper()
                break
            else:
                print("Invalid matrix.  Matrix is either AQ for Aqueous or SD for Solid.")

        cond_samples = []
        for sample in generate_samples(n):
            cond: float = random.uniform(1, 1000)
            cond_samples.append((sample, cond))

        generate_csv(cond_samples, matrix)
        print("Sample Data has been compiled in a file called 'sample_data.csv'")

        user_filename = "sample_data.csv"

    else: #Read an existing file
        while True:
            user_filename: str = str(input("Enter name of file you would like to process (ex. 'example_data.csv'): "))
            try:
                with open(user_filename, mode="r") as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    if headers == ["Sample Number", "Matrix", "Conductivity"]:
                        print(f"Opening '{user_filename}'......")
                        break
                    else:
                        print(f"'{user_filename}' missing expected headers.")
            except FileNotFoundError:
                print(f"file '{user_filename}' not found.")

    #Do you want TSS or Resistivity Data?
    while True:
        t_or_r: str = input("Would you like to see TSS or Resistivity data? To end program, type 'END' ").lower()
        if t_or_r == "tss":
            generate_tss(user_filename)
            print("Sample data has been compiled in a file called 'tss_data.csv'")
            #break
        elif t_or_r == "resistivity":
            generate_resist(user_filename)
            print("Sample data has been compiled in a file called 'res_data.csv'")
            #break
        elif t_or_r == "end":
            sys.exit("Goodbye")
        else:
            print("Invalid operation, please enter TSS, Resistivity, or End")


if __name__ == "__main__":
    main()
