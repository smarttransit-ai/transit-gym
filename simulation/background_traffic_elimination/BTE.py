import pickle

INTERVAL = 60
PATH = './background_traffic_elimination'

class BTE:
    def __init__(self, traci):
        self.traci = traci
        self.edge_data = pickle.load(open('{}/filtered_edge_data.pkl'.format(PATH), 'rb'))

    def update(self):
        step = int(self.traci.simulation.getTime())
        if ((step % INTERVAL == 0) & (step in self.edge_data)):
            for item in self.edge_data[step]:
                self.traci.edge.setMaxSpeed(item['edge_id'], item['edge_speed'])