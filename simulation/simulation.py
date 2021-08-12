import numpy as np
import simpy


class Cashier(object):
    def __init__(self, env, start_time, end_time, proc_time):
        self.env = env
        self.resource = simpy.Resource(env, 1)
        self.open = False
        self.start_time = start_time * 60
        self.end_time = end_time * 60
        self.proc_time = proc_time
    
    def proc(self, customer):
        customer.stats.process = self.env.now
        # proc_time +-5 sec/prod
        process_time = customer.prods * np.random.triangular(self.proc_time - 5, self.proc_time, self.proc_time + 5) / 60
        yield self.env.timeout(process_time)

    def schedule(self):
        day_in_min = 24 * 60
        while True:
            # open
            time_left = (self.start_time - self.env.now) % day_in_min
            yield self.env.timeout(time_left)
            self.open = True
            # close
            time_left = (self.end_time - self.env.now) % day_in_min
            yield self.env.timeout(time_left)
            self.open = False


class CustomerStat(object):
    arrival = None
    queue = None
    process = None
    leave = None


class Customer(object):
    id = 0
    def __init__(self, prods, arrival):
        Customer.id += 1
        self.id = Customer.id
        self.prods = prods
        self.stats = CustomerStat()
        self.stats.arrival = arrival
    
    def get_stats(self):
        return [
            self.stats.arrival,
            self.stats.queue,
            self.stats.process,
            self.stats.leave,
        ]


def p_buy(env, customer, cashiers):
    while True:
        available_cashiers = [cashier for cashier in cashiers if cashier.open]
        if any(available_cashiers):
            break
        # wait 2 for cashier
        yield env.timeout(2)
    customer.stats.queue = env.now
    # choose queue
    cashier = min(available_cashiers, key=lambda x: len(x.resource.queue))
    with cashier.resource.request() as request:
        # wait
        yield request
        # start process
        yield env.process(cashier.proc(customer))
    # leave
    customer.stats.leave = env.now


def arrival(env, start, rate, cashiers, min_n_prods, max_n_prods, stats):
    # wait arrival
    yield env.timeout(start * 60)
    # start arrivals
    while True:
        # create
        yield env.timeout(np.random.exponential(60/rate))
        if env.now - start * 60 >= 60:
            # stop
            break
        # create customer with random products
        customer = Customer(prods=np.random.uniform(min_n_prods, max_n_prods), arrival=env.now)
        stats.append(customer.stats)
        env.process(p_buy(env, customer, cashiers))


def setup(env, cashier_data, arrival_data, proc_time, min_n_prods, max_n_prods, stats):
    cashiers = [
        Cashier(env, start_time, end_time, proc_time)
        for start_time, end_time in cashier_data
    ]
    # start cashiers
    for cashier in cashiers:
        env.process(cashier.schedule())
    for start_hour, rate in arrival_data:
        env.process(arrival(env, start_hour, rate, cashiers, min_n_prods, max_n_prods, stats))


def main(RANDOM_SEED, SIM_TIME, CASHIER_DATA, ARRIVAL_DATA, PROC_TIME, MIN_PRODS, MAX_PRODS, stats):
    # Setup and start the simulation
    if RANDOM_SEED is not None:
        np.random.seed(RANDOM_SEED)  # This helps reproducing the results

    # Create an environment and start the setup process
    env = simpy.Environment()
    setup(env, CASHIER_DATA, ARRIVAL_DATA, PROC_TIME, MIN_PRODS, MAX_PRODS, stats)

    # Execute
    env.run(until=SIM_TIME)


def print_results(stats):
    stats = [s for s in stats if s.leave is not None]
    arrival = np.array([s.arrival for s in stats])
    queue = np.array([s.queue for s in stats])
    process = np.array([s.process for s in stats])
    leave = np.array([s.leave for s in stats])
    print(f'total llegadas: {arrival.shape[0]}')
    wait_time = np.average(process - queue)
    print(f'tiempo de espera: {wait_time:.2f}')
    time_in_system = np.average(leave - arrival)
    print(f'tiempo en sistema: {time_in_system:.2f}')


if __name__ == '__main__':
    RANDOM_SEED = 42
    SIM_TIME = 166 * 60     # Simulation time in minutes
    CASHIER_DATA = [
        *([8, 16] for _ in range(5)),
        *([15, 24] for _ in range(7)),
        *([9, 15] for _ in range(4)),
        *([19, 23.5] for _ in range(4)),
    ]
    ARRIVAL_DATA = [
        [8, 11],[9, 30],[10, 44],[11, 34],[12, 42],[13, 62],[14, 52],[15, 55],[16, 54],[17, 52],[18, 54],[19, 67],[20, 68],[21, 83],[22, 52],
        [32, 38],[33, 78],[34, 100],[35, 93],[36, 112],[37, 107],[38, 66],[39, 56],[40, 52],[41, 64],[42, 52],[43, 89],[44, 72],[45, 83],[46, 44],
        [56, 44],[57, 122],[58, 183],[59, 147],[60, 127],[61, 117],[62, 110],[63, 96],[64, 76],[65, 88],[66, 93],[67, 108],[68, 109],[69, 112],[70, 51],
        [80, 46],[81, 75],[82, 107],[83, 129],[84, 150],[85, 106],[86, 83],[87, 63],[88, 75],[89, 66],[90, 54],[91, 79],[92, 96],[93, 89],[94, 36],
        [104, 36],[105, 68],[106, 114],[107, 104],[108, 100],[109, 112],[110, 109],[111, 92],[112, 77],[113, 97],[114, 75],[115, 89],[116, 102],[117, 84],[118, 38],
        [128, 27],[129, 42],[130, 47],[131, 43],[132, 52],[133, 55],[134, 49],[135, 46],[136, 48],[137, 50],[138, 51],[139, 34],[140, 38],[141, 53],[142, 23],
        [152, 27],[153, 33],[154, 32],[155, 43],[156, 37],[157, 46],[158, 47],[159, 53],[160, 56],[161, 55],[162, 44],[163, 51],[164, 44],[165, 48],[166, 21]
    ]
    PROC_TIME = 25
    MIN_PRODS = 10
    MAX_PRODS = 30
    stats = []
    main(RANDOM_SEED, SIM_TIME, CASHIER_DATA, ARRIVAL_DATA, PROC_TIME, MIN_PRODS, MAX_PRODS, stats)
    print_results(stats)
