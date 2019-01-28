//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
#include "StateMachine.h"

StateMachine::StateMachine() :
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(states[0].lower())]
    //  initializers += ["lastState(ID_{})".format(states[0].upper())]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state.lower()) for state in states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

void StateMachine::init(StateData& stateData)
{
    //[[[cog 
    //  for state in states:
    //    cog.outl("{}.init(stateData);".format(state.lower()))
    //]]]
    //[[[end]]]
}
    
void StateMachine::update()
{
    if (callEntry)
    {
        // only call entry once 
        istate->entry(lastState);
        callEntry = false;
    }
    istate->update();
}

IState* StateMachine::getIStateFromId(StateId stateId)
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = states[-1]
        //  for state in states:
        //    sid = id_of_state[state]
        //    cog.outl("case {}:".format(sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state.lower()))
        //    cog.outl("}")
        //    if state != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]
    }
}

void StateMachine::setNextState(StateId state)
{
    // self transitions also call entry()
    callEntry = true;

    lastState = istate->getId();  
    istate = getIStateFromId(state);
}

