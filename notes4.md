## **SOLID Principles in the Optimization Library**


#### **1️⃣ Single Responsibility Principle (SRP) **

-   Each class has a **clear purpose**:
    -   `OptimizationProblem` handles general optimization logic.
    -   `Constraint` defines constraints separately.
    -   `State` and `DeterministicTransitions` define transition models.
    -   `VRP` extends the optimization model for vehicle routing.
-   The separation of concerns makes it **modular and reusable**.

#### **2️⃣ Open/Closed Principle (OCP) **

-   **New constraints can be added without modifying `Constraint`** due to its abstract nature.
-   **New problem types can be created** by extending `OptimizationProblem` without modifying existing logic.
-   The use of **Enums (`ConstraintType`, `OptimisationType`)** allows easy extension.

#### **3️⃣ Liskov Substitution Principle (LSP) **

-   `Constraint` subclasses can replace `Constraint` seamlessly.
-   `OptimizationProblem` can be extended and substituted.

#### **4️⃣ Interface Segregation Principle (ISP) **
-   `Constraint` is an **abstract base class (ABC)**, enforcing interface segregation.
-   `DeterministicTransitions` also uses `ABC`, keeping interfaces clean.

#### **5️⃣ Dependency Inversion Principle (DIP) **

-   `OptimizationProblem` **depends on abstractions** (`Constraint`, `DecisionVariable`), not concrete implementations.
-   `VRPConstraint` **inherits from `Constraint`**, allowing modular constraint design.