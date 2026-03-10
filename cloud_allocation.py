import heapq

# VM resource requirements
vms = [
    {"cpu": 2, "ram": 4},
    {"cpu": 1, "ram": 2},
    {"cpu": 3, "ram": 4}
]

# Server capacities
servers = [
    {"cpu": 4, "ram": 8},
    {"cpu": 4, "ram": 8}
]

class State:
    def __init__(self, vm_index, servers_state, cost, path):
        self.vm_index = vm_index
        self.servers_state = servers_state
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost


def heuristic(vm_index):
    # remaining VMs heuristic
    return len(vms) - vm_index


def a_star():
    initial_servers = [server.copy() for server in servers]

    start = State(0, initial_servers, 0, [])

    pq = []
    heapq.heappush(pq, (0, start))

    while pq:
        _, current = heapq.heappop(pq)

        if current.vm_index == len(vms):
            return current.path

        vm = vms[current.vm_index]

        for i, server in enumerate(current.servers_state):

            if server["cpu"] >= vm["cpu"] and server["ram"] >= vm["ram"]:

                new_servers = [s.copy() for s in current.servers_state]

                new_servers[i]["cpu"] -= vm["cpu"]
                new_servers[i]["ram"] -= vm["ram"]

                new_path = current.path + [f"VM{current.vm_index+1} -> Server{i+1}"]

                g = current.cost + 1
                h = heuristic(current.vm_index + 1)

                new_cost = g + h

                new_state = State(
                    current.vm_index + 1,
                    new_servers,
                    g,
                    new_path
                )

                heapq.heappush(pq, (new_cost, new_state))

    return None


result = a_star()

print("\nOptimal Allocation using A*:\n")

for step in result:
    print(step)