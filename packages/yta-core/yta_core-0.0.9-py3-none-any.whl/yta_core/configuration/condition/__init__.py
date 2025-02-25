"""
Module to include the different configurations for
the components we are able to build within our app
so we can set the parameters we expect to have or
the ones we need to be able to build each component
according to its type.

We have 2 different types of conditions:
- Mandatory conditions, that has to be met and if
not they raise an exception.
- Optional conditions, that can be met or can be
not, but don't raise an Exception if not met.

So, we have 4 different checkings we can do:
- If we must apply a mandatory condition and it
has to because it has the fields, lets apply it.
- If we must apply a mandatory condition and it
doesn't have the fields to apply it, raise an
Exception.
- If we can apply an optional condition and it
has to, lets apply it.
- If we can apply an optional condition and it
doesn't have the fields to, just ignore it.

Our mandatory conditions start with 'do_' and 
the optional ones with 'can_'.
"""