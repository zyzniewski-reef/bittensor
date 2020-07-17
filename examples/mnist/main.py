from loguru import logger

import argparse
import pickle
import torch
import torchvision

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from opentensor import opentensor_pb2
import opentensor


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


def main(hparams):

    # Training params.
    batch_size_train = 64
    learning_rate = 0.01
    momentum = 0.5
    log_interval = 10

    # Dataset.
    train_loader = torch.utils.data.DataLoader(torchvision.datasets.MNIST(
        root="~/tmp/",
        train=True,
        download=True,
        transform=torchvision.transforms.Compose(
            [torchvision.transforms.ToTensor()])),
                                               batch_size=batch_size_train,
                                               shuffle=True)

    local = Net()
    optimizer = optim.SGD(local.parameters(),
                          lr=learning_rate,
                          momentum=momentum)

    # opentensor identity.
    identity = opentensor.Identity()

    # Build the neuron object.
    neuron = opentensor.Neuron(identity=identity, bootstrap=hparams.bootstrap)
    neuron.start()

    # Keys object.
    # projects from/to opentensor_pb2.Synapse to a variable sized key tensor.
    key_dim = 100
    keymap = opentensor.Keys(key_dim)

    # Gate: object for a trained lookup of keys
    topk = 10  # number of keys to choose for each examples.
    n_keys = 10
    x_dim = 784  # mnist
    gate = opentensor.Gate(x_dim, topk, key_dim)

    # Object for dispatching / combining gated inputs
    dispatcher = opentensor.Dispatcher()

    # Node to serve on metagraph.
    class Mnist(opentensor.Synapse):
        def indef(self):
            shape = [-1, 784]
            dtype = opentensor_pb2.DataType.DT_FLOAT32
            return opentensor_pb2.TensorDef(shape=shape, dtype=dtype)

        def outdef(self):
            shape = [-1, 10]
            dtype = opentensor_pb2.DataType.DT_FLOAT32
            return opentensor_pb2.TensorDef(shape=shape, dtype=dtype)

        def forward(self, key, tensor):
            return local(tensor.view(-1, 1, 28, 28))

        def backward(self, key, tensor):
            pass

    # Subscribe the model encoder to the graph.
    neuron.subscribe(Mnist())

    # Build summary writer for tensorboard.
    writer = SummaryWriter(log_dir='./runs/' + identity.public_key())

    def remote(inputs):
        gate_inputs = torch.flatten(inputs, start_dim=1)

        # Get synapses from the metagraph.
        # and map synapses to torch keys.
        synapses = neuron.synapses()  # List[opentensor_pb2.Synapse]))
        keys = keymap.toKeys(synapses)  # (n_keys, key_dim)

        # Learning a map from the gate_inputs to keys
        # gates[i, j] = score for the jth key for input i
        gates = gate(gate_inputs, keys, topk=min(len(keys), topk))

        # Dispatch data to inputs for each key.
        # when gates[i, j] == 0, the key j does not recieve input i
        dispatch = dispatcher.dispatch(inputs, gates)  # List[(?, 784)]

        # Query the network by mapping from keys to synapse endpoints.
        # results = list[torch.Tensor], len(results) = len(keys)
        synapses = keymap.toSynapses(keys)  # List[opentensor_pb2.Synapse]
        query = neuron(dispatch, synapses)  # List[(?, 748)]

        weights = neuron.getweights(synapses)
        weights = (0.99) * weights + 0.01 * torch.mean(gates, dim=0)
        neuron.setweights(synapses, weights)

        # Join results using gates to combine inputs.
        return dispatcher.combine(query, gates).view(-1,
                                                     10)  # (batch_size, 10)

    def train(epoch, global_step):
        local.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()

            # join the network outputs.
            local_output = local(data)
            remote_output = remote(data)

            output = local_output + remote_output

            loss = F.nll_loss(output, target)
            loss.backward()

            optimizer.step()
            global_step += 1

            if batch_idx % log_interval == 0:
                writer.add_scalar('n_peers', len(neuron.metagraph.peers),
                                  global_step)
                writer.add_scalar('n_synapses', len(neuron.metagraph.synapses),
                                  global_step)
                writer.add_scalar('Loss/train', float(loss.item()),
                                  global_step)
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))

    epoch = 0
    global_step = 0
    while True:
        train(epoch, global_step)
        epoch += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap',
                        default='',
                        type=str,
                        help="peer to bootstrap")
    hparams = parser.parse_args()
    main(hparams)