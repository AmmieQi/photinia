#!/usr/bin/env python3

"""
@author: xi
@since: 2018-07-03
"""

import argparse
import os

import gym

import photinia as ph
from photinia import deep_rl
from photinia.deep_rl import ddpg


class Agent(ddpg.DDPGAgent):

    def __init__(self, name, state_size, action_size, hidden_size=50):
        super(Agent, self).__init__(
            name,
            ph.placeholder('source_state', (None, state_size)),
            ph.placeholder('target_state', (None, state_size)),
            ph.placeholder('reward', (None,)),
            deep_rl.MLPActor('source_actor', state_size, action_size, hidden_size),
            deep_rl.MLPActor('target_actor', state_size, action_size, hidden_size),
            deep_rl.MLPCritic('source_critic', state_size, action_size, hidden_size * 2),
            deep_rl.MLPCritic('target_critic', state_size, action_size, hidden_size * 2),
            replay_size=10000
        )


def main(args):
    model = Agent('agent', 3, 1)
    ph.initialize_global_variables()
    model.init()

    render = False
    env = gym.make('Pendulum-v0')
    env_noise = deep_rl.NormalNoise(1.0, -env.action_space.high, env.action_space.high)
    for i in range(args.num_loops):
        total_r = 0
        s = env.reset()
        for t in range(1000):
            if render:
                env.render()

            a, = model.predict([s])[0]
            a *= env.action_space.high
            a = env_noise.add_noise(a)
            env_noise.discount()

            s_, r, done, info = env.step(a)

            model.feedback(s, a, r, s_)
            model.train(args.batch_size)

            total_r += r
            s = s_
            if done:
                print('[%d] %f' % (i, total_r))
                if total_r > -300 and i >= 100:
                    render = True
                break
    return 0


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-g', '--gpu', default='0', help='Choose which GPU to use.')
    _parser.add_argument('-b', '--batch-size', type=int, default=64)
    _parser.add_argument('-n', '--num-loops', type=int, default=200)
    _args = _parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = _args.gpu
    exit(main(_args))
