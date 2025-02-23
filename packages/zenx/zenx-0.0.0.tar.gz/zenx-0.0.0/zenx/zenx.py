from keras.src import ops
from keras.src.api_export import keras_export
from keras.src import initializers
from keras.src.optimizers import optimizer

class ZenX(optimizer.Optimizer):
    def __init__(
        self,
        learning_rate=0.001,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-7,
        amsgrad=False,
        initial_accumulator_value=0.1,
        name="ZenX",
        **kwargs,
    ):
        super().__init__(
            learning_rate=learning_rate,
            name=name,
            **kwargs,
        )
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.amsgrad = amsgrad
        self.initial_accumulator_value = initial_accumulator_value
        
    def build(self, var_list):
        if self.built:
            return
        super().build(var_list)
        self._momentums = []
        self._velocities = []
        self._accumulators = []
        initializer = initializers.Constant(self.initial_accumulator_value)
        for var in var_list:
            self._momentums.append(
                self.add_variable_from_reference(
                    reference_variable=var, name="momentum"
                )
            )
            self._accumulators.append(
                self.add_variable(
                    shape=var.shape,
                    initializer=initializer,
                    dtype=var.dtype,
                    name="accumulator",
                )
            )
            self._velocities.append(
                self.add_variable_from_reference(
                    reference_variable=var, name="velocity"
                )
            )
        if self.amsgrad:
            self._velocity_hats = []
            for var in var_list:
                self._velocity_hats.append(
                    self.add_variable_from_reference(
                        reference_variable=var, name="velocity_hat"
                    )
                )

    def update_step(self, gradient, variable, learning_rate):
        lr = ops.cast(learning_rate, variable.dtype)
        gradient = ops.cast(gradient, variable.dtype)
        
        m = self._momentums[self._get_variable_index(variable)]
        v = self._velocities[self._get_variable_index(variable)]

        accumulator = self._accumulators[self._get_variable_index(variable)]
        self.assign_add(accumulator, ops.square(gradient))


        self.assign_add(
            m, ops.multiply(ops.subtract(gradient, m), 1 - self.beta_1)
        )
        self.assign_add(
            v,
            ops.multiply(
                ops.subtract(ops.square(gradient), v), 1 - self.beta_2 
            ),
        )
        if self.amsgrad:
            v_hat = self._velocity_hats[self._get_variable_index(variable)]
            self.assign(v_hat, ops.maximum(v_hat, v))
            v = v_hat
        self.assign_sub(
            variable,
            ops.multiply(
                ops.divide(lr, ops.add(ops.log(ops.add(accumulator, 1)), 1)),  
                ops.divide(m, ops.add(ops.sqrt(v), self.epsilon))
            )
            ),

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "beta_1": self.beta_1,
                "beta_2": self.beta_2,
                "epsilon": self.epsilon,
                "amsgrad": self.amsgrad,
            }
        )
        return config
