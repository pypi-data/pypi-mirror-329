"""
A way of add some kind of structure to the information
we are handling during the building process. Each 
project has 4 different steps, so we have created
separate classes to handle it easily.

- ProjectRaw (the project is just a json within a file
that can be valid or can be not)
- ProjectValidated (the project has been validated from
a file and can be built)
- ProjectProcessed (the project has been processed and
some dynamic fields have been calculated so it is 
completely processable).
- ProjectFinished (the project has finished, but it is
like the ProjectProcessed with a 'finished' status).
"""