"""StateId machine stepper module.

This module provides the base `Stepper` and `StateMachine` classes for traversing state machines during parsing
and generation. Steppers track state transitions and maintain parsing history, while StateMachines manage the
constraints and transitions within the state machine.
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from typing import Any, Self, TypeVar

from pse_core import Edge, StateGraph, StateId

Array_Type = TypeVar("Array_Type")

class Engine(ABC):
    """
    The core engine class that manages the state machine and steppers.
    """

    def __init__(
        self,
        reverse_vocabulary: dict[int, str],
        strict: bool = False,
        multi_token_sampling: bool = True,
        max_resamples: int = 5,
        control_tokens: list[int] = [],
    ) -> None: ...
    """Initialize the engine with a reverse vocabulary (a map of token ids to tokens)."""

    def __call__(self, tokens: Array_Type, scores: Array_Type) -> Array_Type: ...
    """Process logits scores and return the corrected logits."""

    def mask_invalid_tokens(self, scores: Array_Type) -> Array_Type: ...
    """Process logits for a given input and scores"""

    def select_next_tokens(
        self, log_probs: Array_Type, sampler: Callable[[Array_Type], Array_Type]
    ) -> list[list[int]]: ...
    """
    Sample a token from the given log probabilities using the provided sampler.

    Args:
        log_probs: The log probabilities to sample from.
        sampler: The sampler to use.
        kwargs: Additional keyword arguments, passed to the sampler.
    """

    def consume_tokens(
        self, token_ids: list[int], token_healing: bool = False
    ) -> list[int]: ...
    """
    Consume a list of tokens. Returns the advanced tokens, or an empty list if the tokens are not valid.

    If only some of the tokens are valid, only the valid tokens are consumed and returned.
    The invalid tokens are discarded.

    Args:
        token_ids: The list of token ids to consume.
        token_healing: Whether to heal tokens.
    Returns:
        The list of advanced token ids, or an empty list if the tokens are not valid.
    """

    def consume_token(
        self, token_id: int, token_healing: bool = True
    ) -> int | None: ...
    """
    Consume a single token. Returns the advanced token, or None if the token is not valid.

    Args:
        token_id: The token id to consume.
        token_healing: Whether to heal tokens.
    Returns:
        The advanced token id, or None if the token is not valid.
    """

    def consume_text(self, input: str, token_healing: bool = False) -> None: ...
    """
    Consume raw input and advance the engine.

    Args:
        input: The raw input to consume.
        token_healing: Whether to heal tokens.
    """

    def break_into_tokens(self, text: str) -> set[list[str]]: ...
    """Break the input into a list of tokens."""

    def reset(self, hard_reset: bool = False) -> None: ...
    """Reset the engine."""

    @property
    def has_reached_accept_state(self) -> bool: ...
    """Check if the engine has reached an accept state."""

    @property
    def is_within_value(self) -> bool: ...
    """Check if the engine is within a structured state."""

    @property
    def current_state(self) -> str: ...
    """Get the current state of the engine."""

    @property
    def state_machine(self) -> StateMachine | None: ...
    """The current state machine."""

    @state_machine.setter
    def state_machine(self, value: StateMachine | None) -> None: ...
    @property
    def vocabulary(self) -> TrieMap: ...
    """The vocabulary (a map of tokens to token ids)."""

    @property
    def reverse_vocabulary(self) -> dict[int, str]: ...
    """The reverse vocabulary (a map of token ids to tokens)."""

    @property
    def steppers(self) -> list[Stepper]: ...
    """
    The engine's current steppers, which are used to traverse the state machine.
    """
    @steppers.setter
    def steppers(self, value: list[Stepper]) -> None: ...
    @property
    def multi_token_mapping(self) -> dict[int, list[int]]: ...
    """
    The multi token mapping (a map of token ids to lists of token ids).
    """
    @multi_token_mapping.setter
    def multi_token_mapping(self, value: dict[int, list[int]]) -> None: ...

class StateMachine:
    """
    A state machine that manages multiple steppers representing
    different valid states, enabling efficient traversal and minimizing backtracking.
    """

    def __init__(
        self,
        state_graph: StateGraph | None = None,
        start_state: StateId = 0,
        end_states: list[StateId] | None = None,
        is_optional: bool = False,
        is_case_sensitive: bool = True,
    ) -> None: ...
    @property
    def is_optional(self) -> bool:
        """Check if the state machine is optional."""
        ...

    @property
    def is_case_sensitive(self) -> bool:
        """Check if the state machine is case sensitive."""
        ...

    def get_new_stepper(self, state: StateId | None = None) -> Stepper:
        """Get a new stepper for this state machine."""
        ...

    def get_steppers(self, state: StateId | None = None) -> list[Stepper]:
        """Get steppers to traverse the state machine.

        Args:
            state: Optional starting state.

        Returns:
            A list of stepper instances.
        """
        ...

    def get_transitions(self, stepper: Stepper) -> list[tuple[Stepper, StateId]]:
        """Get transitions from the given stepper.

        Args:
            stepper: Stepper to get transitions from.

        Returns:
            A list of tuples containing a stepper, start state, and target state.
        """
        ...

    def get_edges(self, state: StateId) -> list[Edge]:
        """Get edges from the given state."""
        ...

    def branch_stepper(
        self, stepper: Stepper, token: str | None = None
    ) -> list[Stepper]:
        """Branch the stepper into multiple paths.

        Args:
            stepper: Stepper to branch.
            token: Optional token to consider.

        Returns:
            A list of branched steppers.
        """
        ...

    def advance_stepper(self, stepper: Stepper, token: str) -> list[Stepper]:
        """Advance the stepper with the given input token.

        Args:
            stepper: The stepper to advance.
            token: The input token to process.

        Returns:
            A list of updated steppers after advancement.
        """
        ...

    @staticmethod
    def advance_all_basic(steppers: list[Stepper], token: str) -> list[Stepper]:
        """Advance multiple steppers with a token."""
        ...

    @staticmethod
    def advance_all(
        steppers: list[Stepper],
        token: str,
        vocab: TrieMap | None = None,
        token_healing: bool = True,
    ) -> list[StepperDelta]:
        """Advance multiple steppers with a token, supports token healing and parallel processing."""
        ...

    def __eq__(self, other: object) -> bool:
        """Check equality based on the state machine's state graph.

        Args:
            other: The object to compare with.

        Returns:
            True if both state machines are equal; False otherwise.
        """
        ...

    def __str__(self) -> str:
        """Return the string representation of the state machine."""
        ...

    def __repr__(self) -> str:
        """Return a detailed string representation of the state machine."""
        ...

    @property
    def start_state(self) -> StateId:
        """The start state of the state machine."""
        ...
    @start_state.setter
    def start_state(self, value: StateId) -> None: ...
    @property
    def end_states(self) -> list[StateId]:
        """The end states of the state machine."""
        ...
    @end_states.setter
    def end_states(self, value: list[StateId]) -> None: ...
    @property
    def state_graph(self) -> StateGraph:
        """The state transition graph."""
        ...
    @state_graph.setter
    def state_graph(self, value: StateGraph) -> None: ...

class Stepper:
    """
    Base class for state machine steppers.

    A `Stepper` represents a position in a state machine graph and manages transitions
    between states as input is consumed.

    It tracks the current state, transition history, and accumulated values during parsing or generation.
    """

    def __init__(
        self, state_machine: StateMachine, current_state: StateId | None = None
    ) -> None:
        """Initialize the stepper.

        Args:
            state_machine: The state machine to associate with the stepper.
            current_state: The current state of the stepper.
        """
        ...
    def clone(self) -> Self:
        """Create a clone of the stepper.

        Returns:
            A new instance of the stepper with the same state.
        """
        ...

    def consume(self, token: str) -> list[Stepper]:
        """Advance the stepper with the given input token.

        Args:
            token: The token to process.

        Returns:
            A list of updated stepper instances after advancement.
        """
        ...

    def can_accept_more_input(self) -> bool:
        """Indicate whether the stepper can accept more input for the current state.

        Returns:
            True if the stepper can accept more input; False otherwise.
        """
        ...

    def is_within_value(self) -> bool:
        """Determine if the stepper is currently within a value.

        Returns:
            True if in a value; False otherwise.
        """
        ...

    def is_optional(self) -> bool:
        """Check if the stepper is optional."""
        ...

    def should_start_step(self, token: str) -> bool:
        """Determine if a stepper should start with the given input token.

        Args:
            token: The token to process.

        Returns:
            True if the stepper should start; False otherwise.
        """
        ...

    def should_complete_step(self) -> bool:
        """Determine if the stepper should complete.

        Returns:
            True if the stepper should complete; False otherwise.
        """
        ...

    def accepts_any_token(self) -> bool:
        """Check if the state machine accepts any token (i.e., free text).

        Returns:
            True if all tokens are accepted; False otherwise.
        """
        ...

    def get_valid_continuations(self) -> list[str]:
        """Return the set of strings that allow valid continuation from current state.

        Args:
            depth: The current depth in the state machine traversal.

        Returns:
            A list of strings that represent valid continuations from current state.
        """
        ...

    def get_invalid_continuations(self) -> list[str]:
        """
        Return the set of strings that allow invalid continuation from current state.
        Default implementation returns an empty list.

        Returns:
            A list of strings that represent invalid continuations from current state.
        """
        ...

    def has_reached_accept_state(self) -> bool:
        """Check if the stepper has reached an accepted (final) state.

        Returns:
            True if in an accepted state; False otherwise.
        """
        ...

    def add_to_history(self, stepper: Stepper) -> None:
        """Add the stepper to the accepted history."""
        ...

    def start_step(
        self,
        sub_stepper: Stepper,
        target_state: StateId,
        token: str | None = None,
    ) -> Stepper | None:
        """Start a new transition with the given token.

        Args:
            sub_stepper: The stepper handling the current transition.
            target_state: The target state.
            token: Optional token to consider.

        Returns:
            A new stepper instance after starting the transition or None if not possible.
        """
        ...

    def complete_step(
        self,
        sub_stepper: Stepper,
    ) -> list[Stepper]:
        """Complete the current transition.

        Args:
            sub_stepper: The stepper handling the current transition.

        Returns:
            A list of new stepper instances.
        """
        ...

    def step(
        self,
        new_value: str | None = None,
        remaining_input: str | None = None,
    ) -> Stepper:
        """
        Step the stepper with the given input token.

        Args:
            new_value: The new value to set.
            remaining_input: The remaining input to set.
        """
        ...

    def should_branch(self) -> bool:
        """Check if the stepper should branch."""
        ...

    def branch(self, token: str | None = None) -> list[Stepper]:
        """Branch the current stepper into multiple paths.

        Args:
            token: Optional token to consider.

        Returns:
            A list of branched stepper instances.
        """
        ...

    def get_current_value(self) -> Any:
        """Retrieve the accumulated stepper value.

        Returns:
            The current value from transition or history, parsed into appropriate type.
            Returns None if no value is accumulated.
        """
        ...

    def get_raw_value(self) -> str:
        """Retrieve the raw accumulated value as a string.

        Returns:
            The concatenated raw values from history and transitions.
        """
        ...

    # Core properties
    @property
    def state_machine(self) -> StateMachine:
        """The state machine associated with this stepper."""
        ...
    @state_machine.setter
    def state_machine(self, value: StateMachine) -> None: ...
    @property
    def current_state(self) -> StateId:
        """The current state."""
        ...
    @current_state.setter
    def current_state(self, value: StateId) -> None: ...
    @property
    def target_state(self) -> StateId | None:
        """The target state."""
        ...
    @target_state.setter
    def target_state(self, value: StateId | None) -> None: ...

    # Sub-stepper and history
    @property
    def sub_stepper(self) -> Stepper | None:
        """The transition stepper."""
        ...
    @sub_stepper.setter
    def sub_stepper(self, value: Stepper | None) -> None: ...
    @property
    def accepted_history(self) -> list[Stepper]:
        """The history of accepted steppers."""
        ...
    @accepted_history.setter
    def accepted_history(self, value: list[Stepper]) -> None: ...

    # Input tracking
    @property
    def consumed_character_count(self) -> int:
        """The number of consumed characters."""
        ...
    @consumed_character_count.setter
    def consumed_character_count(self, value: int) -> None: ...
    @property
    def remaining_input(self) -> str | None:
        """The remaining input string."""
        ...
    @remaining_input.setter
    def remaining_input(self, value: str | None) -> None: ...

    # Value handling
    @property
    def _raw_value(self) -> str | None:
        """The raw accumulated value as a string."""
        ...
    @_raw_value.setter
    def _raw_value(self, value: str | None) -> None: ...

    # Magic methods
    def __eq__(self, other: object) -> bool:
        """Check equality based on the stepper's state and accumulated value.

        Args:
            other: The object to compare with.

        Returns:
            True if both steppers are equal; False otherwise.
        """
        ...

    def __str__(self) -> str:
        """Return the string representation of the stepper."""
        ...

    def __repr__(self) -> str:
        """Return a detailed string representation of the stepper."""
        ...

class StepperDelta:
    """
    Represents a delta/change in a stepper's state along with the token that caused the change.
    Used for tracking and comparing different possible paths through the state machine.
    """

    def __init__(self, stepper: Stepper, token: str, was_healed: bool) -> None:
        """
        Initialize a StepperDelta.

        Args:
            stepper: The stepper in its new state after consuming a token
            token: The token that was consumed
            was_healed: Whether token healing was applied
        """
        ...

    @property
    def stepper(self) -> Stepper:
        """The stepper in its new state."""
        ...
    @stepper.setter
    def stepper(self, value: Stepper) -> None: ...

    @property
    def token(self) -> str:
        """The token that was consumed."""
        ...
    @token.setter
    def token(self, value: str) -> None: ...

    @property
    def was_healed(self) -> bool:
        """Whether token healing was applied."""
        ...
    @was_healed.setter
    def was_healed(self, value: bool) -> None: ...

    def is_attractive_path(self) -> bool:
        """
        Determine if this path is attractive for further exploration.

        Returns:
            True if the path should be explored further, False otherwise.
        """
        ...

    @staticmethod
    def choose_best_path(steppers: set[StepperDelta]) -> tuple[str, list[Stepper]]:
        """
        Choose the best path from a set of possible paths.

        Args:
            steppers: Set of StepperDelta objects representing possible paths

        Returns:
            A tuple containing the chosen token and list of steppers for that path
        """
        ...

    def __eq__(self, other: object) -> bool:
        """Compare two StepperDelta objects for equality."""
        ...

    def __lt__(self, other: StepperDelta) -> bool:
        """Compare two StepperDelta objects for ordering."""
        ...

class TrieMap:
    """A HAT-trie based map implementation for efficient string-to-value mapping.

    This class provides an efficient implementation of a map data structure
    specifically optimized for string keys using a HAT-trie structure.
    """

    def __init__(self, burst_threshold: int = 1024) -> None: ...
    """Initialize a new TrieMap.

    Args:
        burst_threshold: Optional threshold for the trie's burst operation.
    """

    def insert(self, key: str, value: int) -> None: ...
    """Insert a key-value pair into the map.

    Args:
        key: The string key to insert.
        value: The value to associate with the key.
    """

    def insert_all(self, items: list[tuple[str, int]]) -> TrieMap: ...
    """Insert multiple key-value pairs into the map.

    Args:
        items: List of (key, value) tuples to insert.

    Returns:
        Self for method chaining.
    """

    def erase(self, key: str) -> int: ...
    """Remove a key-value pair from the map.

    Args:
        key: The string key to remove.

    Returns:
        Number of elements removed (0 or 1).
    """

    def get(self, key: str) -> list[int] | None: ...
    """Find the value associated with a key.

    Args:
        key: The string key to look for.

    Returns:
        The associated value if found, None otherwise.
    """

    def get_all(self, keys: list[str]) -> list[list[int]]: ...
    """Get the values associated with multiple keys.

    Args:
        keys: The list of string keys to look for.

    Returns:
        A list of values associated with the keys, or an empty list if the key is not found.
    """

    @property
    def empty(self) -> bool: ...
    """Check if the map is empty.

    Returns:
        True if the map contains no elements, False otherwise.
    """

    @property
    def size(self) -> int: ...
    """Get the number of elements in the map.

    Returns:
        The number of key-value pairs stored in the map.
    """

    def clear(self) -> None: ...
    """Remove all elements from the map."""
