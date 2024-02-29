import matplotlib.pyplot as plt

def create_mean_list(latencies):
    new_latencies = []
    start_index = 0
    increment = 1

    while start_index < len(latencies):
        subset = latencies[start_index:start_index + increment]
        mean_value = sum(subset) / len(subset)
        new_latencies.append(mean_value)
        start_index += increment
        increment += 1

    return new_latencies

def plotLatency(file_path):
    with open(file_path, 'r') as f:
        latencies = [float(line.strip()) for line in f.readlines() if line.strip()]
    
    mean_latencies = create_mean_list(latencies)
    
    clients = list(range(1, len(mean_latencies) + 1))
    
    plt.plot(clients, mean_latencies, marker='o', linestyle='-', color='b')
    
    plt.xlabel('Number of Clients')
    plt.ylabel('Average Latency (seconds)')
    plt.title('Average Latency vs Number of Clients')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    plotLatency('latencies.txt')
