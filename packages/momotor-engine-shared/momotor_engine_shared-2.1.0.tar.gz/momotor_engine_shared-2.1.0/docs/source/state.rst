.. py:module:: momotor.shared.state

========================
``momotor.shared.state``
========================

The :py:mod:`momotor.shared.state` module is used by the workers to maintain a shared state.

Local workers use the :py:class:`~momotor.shared.state.LocalState` implementation as a 'dummy' implementation,
since local workers do not need access to any shared state.

Workers connected to the broker use a subclass of the abstract
:py:class:`~momotor.shared.state.StateABC` that implements connecting to the broker to exchange the state.

The implementation on the broker subclasses :py:class:`~momotor.shared.state.LocalState`.

Class documentation
===================

.. autoclass:: momotor.shared.state.StateABC
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.state.LocalState
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.state.LockFailed
   :members:
