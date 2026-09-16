# Spring Banking Demo Testbed

This testbed service demonstrates realistic enterprise Java banking code with intentional edge-case blindspots:
1. `TransferService.java`: Lacks transaction rollback on overdraft, missing concurrency locking.
2. `TransferServiceTest.java`: Only has shallow happy-path unit tests with zero exception or boundary condition verification.
