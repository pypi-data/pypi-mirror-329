import numpy as np
import matplotlib.pyplot as plt

class PiecewiseMotion:
    """
    Simulates motion with piecewise constant acceleration.

    Attributes:
        to (float): Initial time.
        vo (float): Initial velocity.
        xo (float): Initial position.
        tin (list of float): Time intervals for each acceleration segment.
        acc (list of float): Acceleration values for each segment.
        vel (list of float): Computed velocity values at segment endpoints.
        pos (list of float): Computed position values at segment endpoints.
    """

    def __init__(self, to, vo, xo, tin, acc):
        """
        Initializes the motion with given parameters and computes velocity and position.

        Args:
            to (float): Initial time.
            vo (float): Initial velocity.
            xo (float): Initial position.
            tin (list of float): Time intervals for each acceleration segment.
            acc (list of float): Acceleration values for each segment.
        """
        self.to = to
        self.vo = vo
        self.xo = xo
        self.tin = np.array(tin)
        self.acc = np.array(acc)

        self._compute_motion()

    def _compute_motion(self):
        """
        Computes velocity and position at segment endpoints.
        The computed values are stored in `self.vel` and `self.pos`.
        """
        self.vel = [self.vo]
        self.pos = [self.xo]

        for i, t in enumerate(self.tin[:-1]):
            v = self.vel[i] + self.acc[i] * self.tin[i]
            self.vel.append(v)

            x = self.pos[i] + self.vel[i] * self.tin[i] + 0.5 * self.acc[i] * self.tin[i]**2
            self.pos.append(x)

    def get_acceleration(self, t):
        """
        Returns acceleration at a given time.

        Args:
            t (float): Time at which acceleration is needed.

        Returns:
            float: Acceleration value at time `t`. Returns 0 if `t` is out of range.
        """
        t_curr = self.to
        for i, t_int in enumerate(self.tin):
            if t_curr <= t < t_curr + t_int:
                return self.acc[i]
            t_curr += t_int
        return 0  # If t exceeds the defined intervals, assume zero acceleration

    def get_velocity(self, t):
        """
        Returns velocity at a given time.

        Args:
            t (float): Time at which velocity is needed.

        Returns:
            float: Velocity value at time `t`. Returns the last velocity if `t` exceeds the range.
        """
        t_curr = self.to
        v_curr = self.vo

        for i, t_int in enumerate(self.tin[:-1]):
            if t_curr <= t < t_curr + t_int:
                dt = t - t_curr
                return v_curr + self.acc[i] * dt
            t_curr += t_int
            v_curr = self.vel[i + 1]

        return self.vel[-1]  # Return last known velocity if t exceeds the range

    def get_position(self, t):
        """
        Returns position at a given time.

        Args:
            t (float): Time at which position is needed.

        Returns:
            float: Position value at time `t`. Returns the last position if `t` exceeds the range.
        """
        t_curr = self.to
        x_curr = self.xo
        v_curr = self.vo

        for i, t_int in enumerate(self.tin[:-1]):
            if t_curr <= t < t_curr + t_int:
                dt = t - t_curr
                return x_curr + v_curr * dt + 0.5 * self.acc[i] * dt**2
            t_curr += t_int
            x_curr = self.pos[i + 1]
            v_curr = self.vel[i + 1]

        return self.pos[-1]  # Return last known position if t exceeds the range

    def plot(self, resolution=100):
        """
        Plots acceleration, velocity, and position over time.

        Args:
            resolution (int, optional): Number of time points for smooth plotting. Default is 100.

        Outputs:
            Displays a matplotlib figure with three subplots:
            1. Acceleration vs Time
            2. Velocity vs Time
            3. Position vs Time
        """
        t_vals = np.linspace(self.to, self.to + sum(self.tin), resolution)
        a_vals = [self.get_acceleration(t) for t in t_vals]
        v_vals = [self.get_velocity(t) for t in t_vals]
        x_vals = [self.get_position(t) for t in t_vals]

        fig, axs = plt.subplots(3, 1, figsize=(8, 8))

        axs[0].plot(t_vals, a_vals, label='Acceleration a(t)', color='r')
        axs[0].set_ylabel('Acceleration')
        axs[0].legend()
        axs[0].grid()

        axs[1].plot(t_vals, v_vals, label='Velocity v(t)', color='g')
        axs[1].set_ylabel('Velocity')
        axs[1].legend()
        axs[1].grid()

        axs[2].plot(t_vals, x_vals, label='Position x(t)', color='b')
        axs[2].set_xlabel('Time t')
        axs[2].set_ylabel('Position')
        axs[2].legend()
        axs[2].grid()

        plt.tight_layout()
        plt.show()
