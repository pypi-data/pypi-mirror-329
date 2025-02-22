# randomix - Random Jax utilities

Miscellaneous things related to jax and random numbers.

For now, just the Keyer class.

(This package is an experiment with aider, uv, and
what it takes to ship a pypi package)

## Keyer

The `randomix.Keyer` class handles jax.random.PRNGKey state
storage within a single jit context and makes it easy to split
off either single new keys or arrays of keys from the contained
key.

Similar to e.g. [treex.KeySeq](https://cgarciae.github.io/treex/api/KeySeq/)
but slightly more convenient API. (I've seen this basic concept
in other places as well).

Usage:

        key = jax.random.key(42)  # Create a PRNG key through the new Jax API

        keyer = randomix.Keyer(key)

        other_key = keyer()  # Split a new key, update key held inside keyer

        more_keys = keyer((3, 2))  # Get keys with a shape

Note that you should not pass a keyer around jit borders or vmap lambdas
or anything like that; just pass the split keys.

Open question: would it be convenient to just mirror *all* the `jax.random`
methods that take key as an argument to this class?

## Note: New Typed Keys

The new typed keys in JAX are represented as scalar arrays with a special RNG dtype that
satisfies `jnp.issubdtype(key.dtype, jax.dtypes.prng_key)`. This library ensures that the keys
are of the new typed format and provides methods to split them into sub-keys based on a given shape.

For more information on the new typed keys, see the JAX documentation:
[https://docs.jax.dev/en/latest/jep/9263-typed-keys.html#notes-for-jax-library-authors](https://docs.jax.dev/en/latest/jep/9263-typed-keys.html#notes-for-jax-library-authors)

## Version

0.1.1
