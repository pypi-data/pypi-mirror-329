import jax
import jax.random as random
from jax import dtypes

def ensure_typed_key_array(key) -> jax.Array:
    if dtypes.issubdtype(key.dtype, dtypes.prng_key):
        return key
    else:
        raise TypeError("New-style typed JAX PRNG keys required")

class Keyer:
    """
    A class to manage and split JAX PRNG keys using the new typed keys.

    The new typed keys in JAX are represented as scalar arrays with a special RNG dtype that
    satisfies `jnp.issubdtype(key.dtype, jax.dtypes.prng_key)`. This class ensures that the keys
    are of the new typed format and provides methods to split them into sub-keys based on a given shape.

    For more information on the new typed keys, see the JAX documentation:
    https://docs.jax.dev/en/latest/jep/9263-typed-keys.html#notes-for-jax-library-authors

    Attributes:
        key (jax.Array): The current JAX PRNG key.
    """

    def __init__(self, key):
        """
        Initializes the Keyer with a JAX PRNG key.

        Args:
            key (jax.Array): The initial JAX PRNG key.

        Raises:
            TypeError: If the provided key is not a new-style typed JAX PRNG key.
        """
        self.key = ensure_typed_key_array(key)

    def __call__(self, shape=None):
        """
        Splits the current key into sub-keys based on the provided shape.

        Args:
            shape (tuple, optional): The shape of the sub-keys to generate. If None, a single sub-key is generated.

        Returns:
            tuple: A tuple of sub-keys if a shape is provided, otherwise a single sub-key.
        """
        if shape is None:
            new_key, self.key = random.split(self.key)
            return new_key
        else:
            num_keys = jax.numpy.prod(jax.numpy.array(shape))
            keys = random.split(self.key, num_keys + 1)
            self.key = keys[-1]
            return jax.numpy.array(keys[:-1]).reshape(shape)
