from seraph import utils
import warnings

class State:
    value = 0

    def __init__(self, **data: dict[str, any]) -> None:
        self.data = utils.DataContainer(**data)

    def __repr__(self) -> str:
        return "<seraph.State with " + str(len(self)) + " substates>"
    
    def __len__(self) -> int:
        return len(self.getSubstates())
    
    def __iter__(self) -> object:
        self.n = -1
        return self
    
    def __next__(self) -> object:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        if not hasattr(self, "substates"):
            self.computeSubstates()
        return self.substates[n]

    def computeSubstates(self) -> None:
        self.substates = self.getSubstates()
    
    def getSubstates(self) -> list[object]:
        raise SyntaxError("Can't use the base State class, must use a StaticState or DynamicState subclass.")
    
    def getAdjustedValue(self, maxDepth: int=10, currentDepth: int=1) -> int:
        substates = self.getSubstates()
        if len(substates) == 0 or currentDepth >= maxDepth:
            return self.value 
        substateValues = [substate.getAdjustedValue(maxDepth, currentDepth) for substate in substates]
        return sum(substateValues)
    
    def foresee(self, maxDepth: int=10) -> dict[object: int]:
        paths = {}
        for substate in self:
            paths[substate] = substate.getAdjustedValue(maxDepth=maxDepth)
        return paths

class StaticState(State):
    def __init__(self, value: int, *substates: list[State], **data: dict[str: any]) -> None:
        State.__init__(self, **data)
        self.value = value
        self.substates = substates
    
    def getSubstates(self) -> list[object]:
        return self.substates
    
class DynamicState(State):
    def __init__(self, value: int, generator: utils.function or None=None, **data: dict[str: any]) -> None:
        State.__init__(self, **data)
        self.value = value

        if hasattr(self, "getSubstates") and generator == None:
            return None
        elif (not hasattr(self, "getSubstates")) and generator != None:
            self.getSubstates = generator
        else:
            raise SyntaxError("Must either subclass a getSubstates method onto the DynamicState or supply a function at init.")
        
class StateMachine:
    def __init__(self, initialState: State, operate: utils.function or None=None) -> None:
        self.state = initialState

        if hasattr(self, "operate") and operate == None:
            return None
        elif (not hasattr(self, "operate")) and operate != None:
            self.getSubstates = operate
        else:
            raise SyntaxError("Must either subclass a operate method onto the StateMachine or supply a function at init.")

    def __repr__(self) -> str:
        return "<seraph.StateMachine>"
    
    def __iter__(self) -> object:
        return self
    
    def __next__(self) -> State:
        