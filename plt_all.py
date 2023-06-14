import numpy as np
import matplotlib.pyplot as plt

# List of directories to process
directory_list = ["./L0.9", "./L0.93", "./L0.97", "./L1.00", "./L1.03", "./L1.06"]

# Initialize lists to store data and axes objects
data_list = []

# Read and process data from each directory
for directory in directory_list:
    file_list = ["280K/rdf.xvg", "310K/rdf.xvg", "340K/rdf.xvg", "370K/rdf.xvg"]
    directory_data = []
    for file_name in file_list:
        # Process data for each file
        x, y = [], []
        with open(f"{directory}/{file_name}") as f:
            for line in f:
                if line.startswith('@') or line.startswith('#'):
                    continue
                cols = line.split()
                if len(cols) == 2:
                    x.append(float(cols[0]))
                    y.append(float(cols[1]))
        temperature = int(file_name.split('K')[0][-3:])
        folder_name = directory.split('/')[1]
        tail_avg = sum(y[-20:]) / 20
        constant = np.log(tail_avg * 10 / 9) * temperature * (-0.008314)
        print(f"Tail average for {file_name}: {tail_avg}")
        print(f"Constant for {file_name}: {constant}")
        print(f"Temperature for {file_name}: {temperature}")
        
        y_modified = [-8.314e-3 * temperature * np.log(val * 10 / 9) - constant for val in y]
        
        directory_data.append((x, y_modified, temperature, folder_name))
    data_list.append(directory_data)

# Plotting
fig, axs = plt.subplots(1, len(directory_list), figsize=(20, 10), sharex=True, sharey=True)

for i, directory_data in enumerate(data_list):
    for x, y, temperature, folder_name in directory_data:
        ax = axs[i]
        ax.set_title(f"{folder_name}")
        ax.set_xlabel('distance (nm)')
        ax.set_ylabel('PMF (kJ/mol)')
        ax.plot(x, y, label=f'{temperature}K', linewidth=0.5)
        ax.grid(True)
        ax.legend()
        

plt.tight_layout()

plt.subplots_adjust(top=0.813, bottom=0.476, left=0.036, right=0.995, hspace=0.20,
                    wspace=0.135)
plt.savefig('test.png', dpi=1200)
plt.show()


