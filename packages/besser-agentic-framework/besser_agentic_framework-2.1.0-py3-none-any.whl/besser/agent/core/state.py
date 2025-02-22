import inspect
import traceback
from collections import deque
from typing import Any, Callable, TYPE_CHECKING

from besser.agent.core.intent.intent import Intent
from besser.agent.core.session import Session
from besser.agent.core.transition import Transition
from besser.agent.exceptions.exceptions import BodySignatureError, ConflictingAutoTransitionError, \
    DuplicatedIntentMatchingTransitionError, EventSignatureError, IntentNotFound, StateNotFound
from besser.agent.exceptions.logger import logger
from besser.agent.library.event.event_library import auto, intent_matched, variable_matches_operation, file_received
from besser.agent.library.event.event_template import event_template
from besser.agent.library.intent.intent_library import fallback_intent
from besser.agent.library.state.state_library import default_body, default_fallback_body
from besser.agent.nlp.intent_classifier.intent_classifier_configuration import IntentClassifierConfiguration, \
    SimpleIntentClassifierConfiguration
from besser.agent.nlp.intent_classifier.intent_classifier_prediction import IntentClassifierPrediction

if TYPE_CHECKING:
    from besser.agent.core.agent import Agent


class State:
    """The State core component of an agent.

    The agent relies on a state machine to define its execution logic. Each state can run a set of actions, and the agent
    can navigate to other states through transitions that are triggered when events occur (e.g. an intent is matched).

    Args:
        agent (Agent): the agent the state belongs to
        name (str): the state's name
        initial (bool): whether the state is initial or not
        ic_config (IntentClassifierConfiguration): the intent classifier configuration of the state

    Attributes:
        _agent (Agent): The agent the state belongs to
        _name (str): The state name
        _initial (bool): Whether the state is initial or not
        _body (Callable[[Session], None]): The state body. It is a callable that takes as argument a
            :class:`~besser.agent.core.session.Session`. It will be run whenever the agent moves to this state.
        _fallback_body (Callable[[Session], None]): The state fallback body. It is a callable that takes as argument a
            :class:`~besser.agent.core.session.Session`. It will be run whenever the agent tries to move to another state,
            but it can't (e.g. an intent is matched but none of the current state's transitions are triggered on that
            intent)
        _ic_config (IntentClassifierConfiguration): the intent classifier configuration of the state
        _transition_counter (int): Count the number of transitions of this state. Used to name the transitions.
        intents (list[Intent]): The state intents, i.e. those that can be matched from a specific state
        transitions (list[Transition]): The state's transitions to other states
    """

    def __init__(
            self,
            agent: 'Agent',
            name: str,
            initial: bool = False,
            ic_config: IntentClassifierConfiguration or None = None
    ):
        self._agent: 'Agent' = agent
        self._name: str = name
        self._initial: bool = initial
        self._body: Callable[[Session], None] = default_body
        self._fallback_body: Callable[[Session], None] = default_fallback_body
        if not ic_config:
            ic_config = SimpleIntentClassifierConfiguration()
        self._ic_config: IntentClassifierConfiguration = ic_config
        self._transition_counter: int = 0
        self.intents: list[Intent] = []
        self.transitions: list[Transition] = []

    @property
    def agent(self):
        """Agent: The state's agent."""
        return self._agent

    @property
    def name(self):
        """str: The state name"""
        return self._name

    @property
    def initial(self):
        """bool: The initial status of the state (initial or non-initial)."""
        return self._initial

    @property
    def ic_config(self):
        """IntentClassifierConfiguration: the intent classifier configuration of the state."""
        return self._ic_config

    def __eq__(self, other):
        if type(other) is type(self):
            return self._name == other.name and self._agent.name == other.agent.name
        else:
            return False

    def __hash__(self):
        return hash((self._name, self._agent.name))

    def _t_name(self):
        """Name generator for transitions. Transition names are generic and enumerated. On each call, a new name is
        generated and the transition counter is incremented for the next name.

        Returns:
            str: a name for the next transition
        """
        self._transition_counter += 1
        return f"t_{self._transition_counter}"

    def set_global(self, intent: Intent):
        """Set state as globally accessible state.

        Args:
            intent (Intent): the intent that should trigger the jump to the global state
        """
        self.agent.global_initial_states.append((self, intent))
        self.agent.global_state_component[self] = [self]
        # Check whether the states from the global component are already in the list
        # Currently only works for linear states
        transitions = self.transitions
        while transitions:
            transition = transitions[0]
            if transition not in self.agent.global_state_component[self]:
                self.agent.global_state_component[self].append(transition.dest)
            transitions = transition.dest.transitions

    def set_body(self, body: Callable[[Session], None]) -> None:
        """Set the state body.

        Args:
            body (Callable[[Session], None]): the body
        """
        body_signature = inspect.signature(body)
        body_template_signature = inspect.signature(default_body)
        if body_signature.parameters != body_template_signature.parameters:
            raise BodySignatureError(self._agent, self, body, body_template_signature, body_signature)
        self._body = body

    def set_fallback_body(self, body: Callable[[Session], None]):
        """Set the state fallback body.

        Args:
            body (Callable[[Session], None]): the fallback body
        """
        body_signature = inspect.signature(body)
        body_template_signature = inspect.signature(default_fallback_body)
        if body_signature.parameters != body_template_signature.parameters:
            raise BodySignatureError(self._agent, self, body, body_template_signature, body_signature)
        self._fallback_body = body

    def _check_global_state(self, dest: 'State'):
        """Add state to global state component if condition is met.

        If the previous state is a global state, add this state to the component's list
        of the global state.

        Args:
            dest (State): the destination state
        """
        if any(self in global_state for global_state in self.agent.global_initial_states):
            self.agent.global_state_component[self].append(dest)
            return
        for global_state in self.agent.global_state_component:
            if self in self.agent.global_state_component[global_state]:
                self.agent.global_state_component[global_state].append(dest)

    def when_event_go_to(self, event: Callable[[Session, dict], bool], dest: 'State', event_params: dict) -> None:
        """Create a new transition on this state.

        When the agent is in a state and a state's transition event occurs, the agent will move to the destination state
        of the transition.

        Args:
            event (Callable[[Session, dict], bool]): the transition event
            dest (State): the destination state
            event_params (dict): the parameters associated to the event
        """
        # TODO: Standardize events
        # event_signature = inspect.signature(event)
        # event_template_signature = inspect.signature(event_template)
        # if event_signature.parameters != event_template_signature.parameters:
        #     raise EventSignatureError(self._agent, event, event_template_signature, event_signature)
        for transition in self.transitions:
            if transition.is_auto():
                raise ConflictingAutoTransitionError(self._agent, self)
        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=event,
                                           event_params=event_params))
        self._check_global_state(dest)

    def go_to(self, dest: 'State') -> None:
        """Create a new `auto` transition on this state.

        This transition needs no event to be triggered, which means that when the agent moves to a state 
        that has an `auto` transition, the agent will move to the transition's destination state 
        unconditionally without waiting for user input. This transition cannot be combined with other
        transitions.

        Args:
            dest (State): the destination state
        """
        if dest not in self._agent.states:
            raise StateNotFound(self._agent, dest)
        if self.transitions:
            raise ConflictingAutoTransitionError(self._agent, self)
        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=auto, event_params={}))
        self._check_global_state(dest)

    def when_intent_matched_go_to(self, intent: Intent, dest: 'State') -> None:
        """Create a new `intent matching` transition on this state.

        When the agent is in a state and an intent is received (the intent is predicted from a user message),
        if the transition event is to receive this particular intent, the agent will move to the transition's destination
        state.

        Args:
            intent (Intent): the transition intent
            dest (State): the destination state
        """
        if intent in self.intents:
            raise DuplicatedIntentMatchingTransitionError(self, intent)
        if intent not in self._agent.intents:
            raise IntentNotFound(self._agent, intent)
        if dest not in self._agent.states:
            raise StateNotFound(self._agent, dest)
        for transition in self.transitions:
            if transition.is_auto():
                raise ConflictingAutoTransitionError(self._agent, self)
        event_params = {'intent': intent}
        self.intents.append(intent)
        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=intent_matched,
                                           event_params=event_params))
        self._check_global_state(dest)

    def when_no_intent_matched_go_to(self, dest: 'State') -> None:
        """Create a new `no intent matching` transition on this state.

        When the agent is in a state and no fitting intent is received (the intent is predicted from a user message), 
        the agent will move to the transition's destination
        state. If no other transition is specified, the agent will wait for a user message regardless.

        Args:
            dest (State): the destination state
        """
        event_params = {'intent': fallback_intent}
        # self.intents.append(fallback_intent)
        if dest not in self._agent.states:
            raise StateNotFound(self._agent, dest)
        for transition in self.transitions:
            if transition.is_auto():
                raise ConflictingAutoTransitionError(self._agent, self)
        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=intent_matched,
                                           event_params=event_params))

    def when_variable_matches_operation_go_to(
            self,
            var_name: str,
            operation: Callable[[Any, Any], bool],
            target: Any,
            dest: 'State'
    ) -> None:
        """Create a new `variable_matches_operation` transition on this state.

        When the agent is in a state and the operation on the specified session variable and target value returns true,
        then the agent moves to the specified destination state.

        Args:
            var_name (str): the name of the stored variable in the session storage
            operation (Callable[[Any, Any], bool]): the comparison operation to be done on the stored and target value
            target (Any): the target value to which will be used in the operation with the stored value
            dest (State): the destination state
        """
        if dest not in self._agent.states:
            raise StateNotFound(self._agent, dest)
        for transition in self.transitions:
            if transition.is_auto():
                raise ConflictingAutoTransitionError(self._agent, self)
        event_params = {'var_name': var_name, 'operation': operation, 'target': target}

        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=variable_matches_operation,
                                           event_params=event_params))

    def when_file_received_go_to(self, dest: 'State', allowed_types: list[str] or str = None) -> None:
        """Create a new `file received` transition on this state.

        When the agent is in a state and a file is received the agent will move to the transition's destination
        state. If no other transition is specified, trigger the fallback state.

        Args:
            dest (State): the destination state
            allowed_types (list[str] or str, optional): the allowed file types, non-conforming types will cause a
            fallback message
        """
        if dest not in self._agent.states:
            raise StateNotFound(self._agent, dest)
        for transition in self.transitions:
            if transition.is_auto():
                raise ConflictingAutoTransitionError(self._agent, self)
        event_params = {}
        if allowed_types:
            event_params = {'allowed_types': allowed_types}
        self.transitions.append(Transition(name=self._t_name(), source=self, dest=dest, event=file_received,
                                           event_params=event_params))

    def receive_intent(self, session: Session) -> None:
        """Receive an intent from a user session (which is predicted from the user message).

        When receiving an intent it looks for the state's transition whose trigger event is to match that intent.
        The fallback body is run when the received intent does not match any transition intent (i.e. fallback intent).

        Args:
            session (Session): the user session that sent the message
        """
        predicted_intent: IntentClassifierPrediction = session.predicted_intent
        if predicted_intent is None:
            logger.error("Something went wrong, no intent was predicted")
            return
        for transition in self.transitions:
            if transition.is_event_true(session):
                session.flags['predicted_intent'] = False
                session.move(transition)
                return
        session.flags['predicted_intent'] = False
        if predicted_intent.intent == fallback_intent:
            # When no transition is activated, run the fallback body of the state
            logger.info(f"[{self._name}] Running fallback body {self._fallback_body.__name__}")
            try:
                self._fallback_body(session)
            except Exception as _:
                logger.error(f"An error occurred while executing '{self._fallback_body.__name__}' of state "
                              f"'{self._name}' in agent '{self._agent.name}'. See the attached exception:")
                traceback.print_exc()

    def receive_file(self, session: Session) -> None:
        """Receive a file from a user session.

        When receiving a file it looks for the state's transition whose trigger event is to receive a file.
        The fallback body is when no file transition was defined.

        Args:
            session (Session): the user session that sent the message
        """
        for transition in self.transitions:
            if transition.is_event_true(session):
                session.flags['file'] = False
                session.move(transition)
                return
        session.flags['file'] = False
        # When no transition is activated, run the fallback body of the state
        logger.info(f"[{self._name}] Running fallback body {self._fallback_body.__name__}")
        try:
            self._fallback_body(session)
        except Exception as _:
            logger.error(f"An error occurred while executing '{self._fallback_body.__name__}' of state"
                          f"'{self._name}' in agent '{self._agent.name}'. See the attached exception:")
            traceback.print_exc()

    def receive_event(self, session: Session) -> None:
        """Receive an event from a user session.

        When receiving an event it looks for the state's transition whose trigger event matches the first event.
        If not we pop the current event and check for the next one.
        The passed items are discarded, unless no transition is made.

        Args:
            session (Session): the user session that received the event
        """
        # TODO: Decide policy to remove events
        fallback_deque = deque()
        while session.events:
            for transition in self.transitions:
                if transition.is_event_true(session):
                    session.event = session.events.pop()
                    session.flags['event'] = False
                    session.move(transition)
                    return
            fallback_deque.appendleft(session.events.pop())
        session.events.extend(fallback_deque)
        session.flags['event'] = False

        # When no transition is activated and the event not broadcasted, run the fallback body of the state
        # logger.info(f"[{self._name}] Running fallback body {self._fallback_body.__name__}")
        # try:
        #     self._fallback_body(session)
        # except Exception as _:
        #     logger.error(f"An error occurred while executing '{self._fallback_body.__name__}' of state"
        #                   f"'{self._name}' in agent '{self._agent.name}'. See the attached exception:")

    def _check_next_transition(self, session: Session) -> None:
        """Check whether the first defined transition of the state is an `auto` transition, and if so, move to its
        destination state.

        This method is intended to be called after running the body of a state.

        Args:
            session (Session): the user session
        """
        # Check auto transition
        if self.transitions[0].is_auto():
            session.move(self.transitions[0])
            return

        for next_transition in self.transitions:
            if next_transition.event == intent_matched:
                # If the next transition is an intent_matched, we return to await the user message
                return
            elif next_transition.is_event_true(session):
                session.move(next_transition)
                return

    def run(self, session: Session) -> None:
        """Run the state (i.e. its body). After running the body, check if the first defined transition of the state is
        an `auto` transition, and if so, move to its destination state.

        Args:
            session (Session): the user session
        """
        logger.info(f"[{self._name}] Running body {self._body.__name__}")
        try:
            self._body(session)
        except Exception as _:
            logger.error(f"An error occurred while executing '{self._body.__name__}' of state '{self._name}' in agent '"
                          f"{self._agent.name}'. See the attached exception:")
            traceback.print_exc()
        self._check_next_transition(session)
