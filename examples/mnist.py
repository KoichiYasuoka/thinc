from __future__ import print_function
import plac

from thinc import datasets
from thinc.base import Network
from thinc.vec2vec import ReLu, Softmax
from thinc.util import score_model


class ReLuMLP(Network):
    Hidden = ReLu
    Output = Softmax
    width = 64
    depth = 3

    def setup(self, nr_out, nr_in, **kwargs):
        for i in range(self.depth):
            self.layers.append(self.Hidden(self.width, nr_in))
            nr_in = self.width
        self.layers.append(self.Output(nr_out, nr_in))


def main(batch_size=128, nb_epoch=8, nb_classes=10):
    model = ReLuMLP(10, 784)
    train_data, check_data, test_data = datasets.keras_mnist()
    
    with model.begin_training(train_data) as (trainer, optimizer):
        for examples, truth in trainer.iterate(model, train_data, check_data):
            guess, update = model.begin_update(examples)

            gradient, loss = model.get_gradient(guess, truth)
            optimizer.set_loss(loss)

            finish_update(gradient, optimizer, L2=trainer.L2)

    print('Test score:', score_model(model, test_data))


if __name__ == '__main__':
    if 1:
        plac.call(main)
    else:
        import cProfile
        import pstats
        cProfile.runctx("main()", globals(), locals(), "Profile.prof")
        s = pstats.Stats("Profile.prof")
        s.strip_dirs().sort_stats("time").print_stats()
