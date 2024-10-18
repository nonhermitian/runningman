# runningman
runningman is Qiskit Runtime interface that aids in building vertically and maintaining a platform agnostic interface

## About

Executing on IBM Quantum systems is now done through the Qiskit Runtime, and the ubiqitous `backend.run()` will be removed from their service.  For those looking to build on top of Qiskit this has several consequences.  First, supporting multiple hardware providers is now more complicated, and boilerplate code must be written to handle differing interfaces. Second, for packages that require backend knowledge, e.g. for things like error suppression and mitigation techniques, one must either carry two pieces of information around (backend instance and Runtime executor for IBM systems) or use the executor in place of a backend and extract the details from there.  This would again require a bit of machinery to do this; code that would have to be reproduced for each package / repo that needs it.

runningman is a package that takes care of a lot of this machinery in a single location.  Its primary goal is to enable `backend.run()` to work on IBM Quantum systems via a wrapper; once again allowing for the backend to be the sole variable needed for getting device characteristics as well as performing the execution, and making it easier to work across providers that leverage Qiskit.

