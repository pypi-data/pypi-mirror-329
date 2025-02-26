from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Literal, Self, Tuple, Type, get_args

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from velora.buffer import BatchExperience, Experience, ReplayBuffer
from velora.gym import add_core_env_wrappers
from velora.models.lnn.ncp import LiquidNCPNetwork
from velora.noise import OUNoise
from velora.utils.torch import soft_update

CheckpointLiteral = Literal[
    "state_dim",
    "n_neurons",
    "action_dim",
    "buffer_size",
    "device",
    "actor",
    "critic",
    "actor_target",
    "critic_target",
    "actor_optim",
    "critic_optim",
]


class DDPGActor(nn.Module):
    """
    A Liquid NCP Actor Network for the DDPG algorithm.
    """

    def __init__(
        self,
        num_obs: int,
        n_neurons: int,
        num_actions: int,
        *,
        device: torch.device | None = None,
    ):
        """
        Parameters:
            num_obs (int): the number of input observations
            n_neurons (int): the number of hidden neurons
            num_actions (int): the number of actions
            device (torch.device, optional): the device to perform computations on
        """

        super().__init__()

        self.ncp = LiquidNCPNetwork(
            in_features=num_obs,
            n_neurons=n_neurons,
            out_features=num_actions,
            device=device,
        )

    def forward(
        self, obs: torch.Tensor, hidden: torch.Tensor | None = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Performs a forward pass through the network.

        Parameters:
            obs (torch.Tensor): the batch of state observations
            hidden (torch.Tensor, optional): the hidden state

        Returns:
            actions (torch.Tensor): the action predictions.
            hidden (torch.Tensor): the new hidden state.
        """
        actions, new_hidden = self.ncp(obs, hidden)
        scaled_actions = torch.tanh(actions)  # Bounded: [-1, 1]
        return scaled_actions, new_hidden


class DDPGCritic(nn.Module):
    """
    A Liquid NCP Critic Network for the DDPG algorithm.
    """

    def __init__(
        self,
        num_obs: int,
        n_neurons: int,
        num_actions: int,
        *,
        device: torch.device | None = None,
    ):
        """
        Parameters:
            num_obs (int): the number of input observations
            n_neurons (int): the number of hidden neurons
            num_actions (int): the number of actions
            device (torch.device, optional): the device to perform computations on
        """
        super().__init__()

        self.ncp = LiquidNCPNetwork(
            in_features=num_obs + num_actions,
            n_neurons=n_neurons,
            out_features=1,  # Q-value output
            device=device,
        )

    def forward(
        self,
        obs: torch.Tensor,
        actions: torch.Tensor,
        hidden: torch.Tensor | None = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Performs a forward pass through the network.

        Parameters:
            obs (torch.Tensor): the batch of state observations
            actions (torch.Tensor): the batch of actions
            hidden (torch.Tensor, optional): the hidden state

        Returns:
            q_values (torch.Tensor): the Q-Value predictions.
            hidden (torch.Tensor): the new hidden state.
        """
        inputs = torch.cat([obs, actions], dim=-1)

        q_values, new_hidden = self.ncp(inputs, hidden)
        return q_values, new_hidden


class LiquidDDPG:
    """
    A Liquid variant of the Deep Deterministic Policy Gradient (DDPG)
    algorithm from the paper: [Continuous Control with Deep Reinforcement Learning](https://arxiv.org/abs/1509.02971).

    !!! note "Decision nodes"

        `inter` and `command` neurons are automatically calculated using:

        ```python
        command_neurons = max(int(0.4 * n_neurons), 1)
        inter_neurons = n_neurons - command_neurons
        ```
    """

    def __init__(
        self,
        state_dim: int,
        n_neurons: int,
        action_dim: int,
        *,
        optim: Type[optim.Optimizer] = optim.Adam,
        buffer_size: int = 100_000,
        actor_lr: float = 1e-4,
        critic_lr: float = 1e-3,
        device: torch.device | None = None,
    ) -> None:
        """
        Parameters:
            state_dim (int): number of inputs (sensory nodes)
            n_neurons (int): number of decision nodes (inter and command nodes).
            action_dim (int): number of outputs (motor nodes)
            optim (Type[torch.optim.Optimizer], optional): the type of `PyTorch`
                optimizer to use
            buffer_size (int, optional): the maximum size of the ReplayBuffer
            actor_lr (float, optional): the actor optimizer learning rate
            critic_lr (float, optional): the critic optimizer learning rate
            device (torch.device, optional): the device to perform computations on
        """
        self.state_dim = state_dim
        self.n_neurons = n_neurons
        self.action_dim = action_dim
        self.buffer_size = buffer_size
        self.device = device

        self.actor = DDPGActor(
            self.state_dim,
            self.n_neurons,
            self.action_dim,
            device=self.device,
        ).to(self.device)

        self.critic = DDPGCritic(
            self.state_dim,
            self.n_neurons,
            self.action_dim,
            device=self.device,
        ).to(self.device)

        self.actor_target = deepcopy(self.actor)
        self.critic_target = deepcopy(self.critic)

        self.actor_optim = optim(self.actor.parameters(), lr=actor_lr)
        self.critic_optim = optim(self.critic.parameters(), lr=critic_lr)

        self.loss = nn.MSELoss()
        self.buffer = ReplayBuffer(capacity=buffer_size, device=device)
        self.noise = OUNoise(action_dim, device=device)

    def _update_target_networks(self, tau: float) -> None:
        """
        Helper method. Performs a soft update on the target networks.

        Parameters:
            tau (float): a soft decay coefficient for updating the target network
                weights
        """
        soft_update(self.actor, self.actor_target, tau=tau)
        soft_update(self.critic, self.critic_target, tau=tau)

    def _update_critic(self, batch: BatchExperience, gamma: float) -> float:
        """
        Helper method. Performs a Critic Network update.

        Parameters:
            batch (BatchExperience): an object containing a batch of experience
                with `(states, actions, rewards, next_states, dones)` from the
                buffer
            gamma (float): the reward discount factor

        Returns:
            critic_loss (float): the Critic's loss value.
        """
        with torch.no_grad():
            next_states = batch.next_states
            next_actions, _ = self.actor_target(next_states)
            target_q, _ = self.critic_target(next_states, next_actions)
            target_q = batch.rewards + (1 - batch.dones) * gamma * target_q

        current_q, _ = self.critic(batch.states, batch.actions)
        critic_loss: torch.Tensor = self.loss(current_q, target_q)

        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        return critic_loss.item()

    def _update_actor(self, states: torch.Tensor) -> float:
        """
        Helper method. Performs an Actor Network update.

        Parameters:
            states (torch.Tensor): a batch of state experiences from the buffer

        Returns:
            actor_loss (float): the Actor's loss value.
        """
        next_actions, _ = self.actor(states)
        actor_q, _ = self.critic(states, next_actions)
        actor_loss: torch.Tensor = -actor_q.mean()

        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()

        return actor_loss.item()

    def _train_step(self, batch_size: int, gamma: float) -> Tuple[float, float]:
        """
        Helper method. Performs a single training step.

        Parameters:
            batch_size (int): number of samples in a batch
            gamma (float): the reward discount factor

        Returns:
            critic_loss (float): the critic loss.
            actor_loss (float): the actor loss.
        """
        if len(self.buffer) < batch_size:
            return

        batch = self.buffer.sample(batch_size)

        critic_loss = self._update_critic(batch, gamma)
        actor_loss = self._update_actor(batch.states)

        return critic_loss, actor_loss

    def train(
        self,
        env: gym.Env,
        batch_size: int,
        *,
        n_episodes: int = 1000,
        max_steps: int = 1000,
        noise_scale: float = 0.1,
        gamma: float = 0.99,
        tau: float = 0.005,
        window_size: int = 100,
    ) -> List[float]:
        """
        Trains the agent on a Gymnasium environment using a `ReplayBuffer`.

        Parameters:
            env (gym.Env): the Gymnasium environment to train on
            batch_size (int): the number of features in a single batch
            n_episodes (int, optional): the total number of episodes to train for
            max_steps (int, optional): the total number of steps per episode
            noise_scale (float, optional): the exploration noise added when
                selecting an action
            gamma (float, optional): the reward discount factor
            tau (float, optional): the soft update factor used to slowly update
                the target networks
            window_size (int, optional): controls the episode rate for displaying
                information to the console and for calculating the reward moving
                average

        Returns:
            ep_rewards (List[float]): a list of episode rewards.
        """
        if not isinstance(env.action_space, gym.spaces.Box):
            raise EnvironmentError(
                f"Invalid '{env.action_space=}'. Must be 'gym.spaces.Box'."
            )

        env = add_core_env_wrappers(env, self.device)

        episode_rewards = []
        training_started = False

        print(f"{batch_size=}, getting buffer samples.")
        for i_ep in range(n_episodes):
            state, _ = env.reset()

            critic_losses, actor_losses = [], []
            actor_hidden = None

            for _ in range(max_steps):
                action, actor_hidden = self.predict(
                    state,
                    actor_hidden,
                    noise_scale=noise_scale,
                )
                next_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated

                self.buffer.push(
                    Experience(state, action.item(), reward, next_state, done),
                )

                if len(self.buffer) >= batch_size:
                    if not training_started:
                        print("Buffer warmed. Starting training...")
                        training_started = True

                    critic_loss, actor_loss = self._train_step(batch_size, gamma)
                    self._update_target_networks(tau)

                    critic_losses.append(critic_loss)
                    actor_losses.append(actor_loss)

                state = next_state

                if done:
                    episode_rewards.append(info["episode"]["r"].item())
                    break

            if training_started and (i_ep + 1) % window_size == 0:
                avg_reward = np.mean(episode_rewards[-window_size:])
                avg_critic_loss = np.mean(critic_losses)
                avg_actor_loss = np.mean(actor_losses)

                print(
                    f"Episode: {i_ep + 1}/{n_episodes}, "
                    f"Avg Reward: {avg_reward:.2f}, "
                    f"Critic Loss: {avg_critic_loss:.2f}, "
                    f"Actor Loss: {avg_actor_loss:.2f}"
                )

        env.close()
        return episode_rewards

    def predict(
        self,
        state: torch.Tensor,
        hidden: torch.Tensor = None,
        *,
        noise_scale: float = 0.1,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Makes an action prediction using the Actor network with exploration noise.

        Parameters:
            state (torch.Tensor): the current state
            hidden (torch.Tensor, optional): the current hidden state
            noise_scale (float, optional): the exploration noise added when
                selecting an action

        Returns:
            action (torch.Tensor): the action prediction on the given state
            hidden (torch.Tensor): the Actor networks new hidden state
        """
        self.actor.eval()
        with torch.no_grad():
            action, hidden = self.actor(state.unsqueeze(0), hidden)

            if noise_scale > 0:
                # Exploration noise
                noise = self.noise.sample() * noise_scale
                action = torch.clamp(action + noise, min=-1, max=1)

        self.actor.train()
        return action.flatten(), hidden

    def save(self, filepath: str | Path, *, buffer: bool = False) -> None:
        """
        Saves the current model state into a file and optionally the buffer.

        Parameters:
            filepath (str | Path): the location to store the model state
            buffer (bool, optional): a flag for storing the buffer state.
                When `True`, creates a file matching `<filepath>.buffer.<filepath_ext>`
        """
        save_path = Path(filepath)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        checkpoint: Dict[CheckpointLiteral, Any] = {
            "state_dim": self.state_dim,
            "n_neurons": self.n_neurons,
            "action_dim": self.action_dim,
            "buffer_size": self.buffer_size,
            "device": str(self.device),
            "actor": self.actor.state_dict(),
            "critic": self.critic.state_dict(),
            "actor_target": self.actor_target.state_dict(),
            "critic_target": self.critic_target.state_dict(),
            "actor_optim": self.actor_optim.state_dict(),
            "critic_optim": self.critic_optim.state_dict(),
        }
        torch.save(checkpoint, save_path)

        if buffer:
            buffer_path = self.buffer.create_filepath(save_path)
            self.buffer.save(buffer_path)

    @classmethod
    def load(cls, filepath: str | Path, *, buffer: bool = False) -> Self:
        """
        Loads a saved model state with and optionally with a buffer.

        Parameters:
            filepath (str | Path): the location for the saved model state
            buffer (bool, optional): a flag for loading the buffer state.
                When `True`, filename must match `<filepath>.buffer.<filepath_ext>`
        """
        load_path = Path(filepath)
        checkpoint: Dict[CheckpointLiteral, Any] = torch.load(load_path)
        buffer_path = None

        valid_keys = set(get_args(CheckpointLiteral))
        if not all(key in valid_keys for key in checkpoint.keys()):
            raise ValueError(
                "File cannot be loaded. Mismatch between checkpoint keys! Are you loading the right file?"
            )

        # Create new model instance
        model = cls(
            checkpoint["state_dim"],
            checkpoint["n_neurons"],
            checkpoint["action_dim"],
            buffer_size=checkpoint["buffer_size"],
            device=torch.device(checkpoint["device"]),
        )

        # Check buffer valid
        if buffer:
            buffer_path = model.buffer.create_filepath(load_path)

            if not buffer_path.exists():
                raise FileNotFoundError(
                    f"Buffer file '{buffer_path}' does not exist! Try with `buffer=False` instead."
                )

        model.actor.load_state_dict(checkpoint["actor"])
        model.critic.load_state_dict(checkpoint["critic"])
        model.actor_target.load_state_dict(checkpoint["actor_target"])
        model.critic_target.load_state_dict(checkpoint["critic_target"])
        model.actor_optim.load_state_dict(checkpoint["actor_optim"])
        model.critic_optim.load_state_dict(checkpoint["critic_optim"])

        if buffer:
            model.buffer = model.buffer.load(buffer_path)

        print(
            f"Loaded model with:\n"
            f"  state_dim={model.state_dim}, n_neurons={model.n_neurons}, action_dim={model.action_dim}\n"
            f"  optim={type(model.actor_optim).__name__}, device={model.device}\n"
            f"  buffer_size={model.buffer_size:,}, buffer_restored={buffer}"
        )
        return model
