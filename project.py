import random
import csv
import sys


def generate_samples(n):
    #Generate sample numbers in the form "000-n" where n is the number of samples
    return[f"100-{i+1}" for i in range(n)]


def generate_csv(samples, matrix, filename="sample_data.csv"):
    #Write samples and matrix to csv file

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sample Number", "Matrix Type", "Conductivity"]) #Headers
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
            tss = cond * 0.64

            tss_data.append([sample_number, matrix, f"{cond:.2f} μS/cm", f"{tss:.2f} ppm"])

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
                res = (1/cond) * 1000000
                res_data.append([sample_number, matrix, f"{cond:.2f} μS/cm", f"{res:.2f} Ωm"])
                with open(output_filename, mode="w", newline="") as file_out:
                    writer = csv.writer(file_out)
                    writer.writerow(["Sample Number", "Matrix", "Conductivity", "Resistivity"])
                    writer.writerows(res_data)
            elif matrix == "SD":
                res = (1/(10*cond)) * 1000000
                res_data.append([sample_number, matrix, f"{cond:.2f} μS/cm", f"{res:.2f} Ωm"])
                with open(output_filename, mode="w", newline="") as file_out:
                    writer = csv.writer(file_out)
                    writer.writerow(["Sample Number", "Matrix", "Conductivity", "Resistivity"])
                    writer.writerows(res_data)


def main():
    n: int = int(input("How many samples? "))

    #cond: float = random.uniform(1, 1000)

    while True:
        matrix: str = input("What is the sample matrix? (AQ or SD) ").upper()
        if matrix in ["AQ", "SD"]:
            break
        else:
            print("Invalid matrix.  Matrix is either AQ for Aqueous or SD for Solid.")

    #samples = generate_samples(n)
    cond_samples = []
    for sample in generate_samples(n):
        cond: float = random.uniform(1, 1000)
        cond_samples.append((sample, cond))

    print("Sample Numbers & Matrix: ")
    for sample, cond in cond_samples:
        print(f"{sample}, {matrix}, {cond:.2f} μS/cm")

    generate_csv(cond_samples, matrix)
    print("Sample Data has been compiled in a file called 'sample_data.csv'")

    #Do you want TSS or Resistivity Data?
    while True:
        t_or_r: str = input("Would you like to see TSS or Resistivity data? To end program, type 'END' ")
        if t_or_r == "TSS" or t_or_r == "tss":
            generate_tss()
            print("Sample data has been compiled in a file called 'tss_data.csv'")
            #break
        elif t_or_r == "Resistivity":
            generate_resist()
            print("Sample data has been compiled in a file called 'res_data.csv'")
            #break
        elif t_or_r == "END" or t_or_r == "end":
            sys.exit("Goodbye")
        else:
            print("Invalid operation, please enter TSS or Resistivity")


if __name__ == "__main__":
    main()
