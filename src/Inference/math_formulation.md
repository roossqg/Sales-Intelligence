
# Mathematical Formulation

1. Product x Price optimization:

## Mathematical Formulation

The objective is to determine the optimal quantity of each product in order to maximize total profit while respecting budget and capacity constraints.

### Decision Variables

For each product $i$:

$$
q_i = \text{quantity of product } i
$$

where:

$$
q_i \in \mathbb{Z}_{\geq 0}
$$

### Parameters

For each product $i$:

- $p_i$: selling price per unit
- $c_i$: cost per unit
- $w_i$: capacity consumed per unit
- $B$: available budget
- $C_i$: total available capacity per product

The unit profit of product $i$ is:

$$
\pi_i = p_i - c_i
$$

### Objective Function

The objective is to maximize total profit:

$$
\max Z =
\sum_{i=1}^{n}(p_i-c_i)q_i
$$

or equivalently:

$$
\max Z =
\sum_{i=1}^{n}p_iq_i
-
\sum_{i=1}^{n}c_iq_i
$$

### Constraints

#### Budget Constraint

The total cost cannot exceed the available budget:

$$
\sum_{i=1}^{n}c_iq_i \leq B
$$

#### Capacity Constraint

The total capacity consumed cannot exceed the available capacity for each product/class:

$$
\sum_{i=1}^{n}w_iq_i \leq C_i
$$

#### Non-Negativity and Integrality

The quantity of each product must be a non-negative integer:

$$
q_i \in \mathbb{Z}_{\geq 0}
$$

### Complete Optimization Model

The complete model can be written as:

$$
\begin{aligned}
\max_{q_1,\ldots,q_n}
\quad & \sum_{i=1}^{n}(p_i-c_i)q_i \\[4pt]
\text{subject to}
\quad & \sum_{i=1}^{n}c_iq_i \leq B \\[4pt]
& \sum_{i=1}^{n}w_iq_i \leq C_i \\[4pt]
& q_i \in \mathbb{Z}_{\geq 0},
\qquad i=1,\ldots,n
\end{aligned}
$$

### Problem Classification

This is an **Integer Linear Programming (ILP)** problem because:

- The decision variables are integers.
- The objective function is linear.
- All constraints are linear.

If the variables were allowed to take continuous values instead of integer values, the problem would be a standard **Linear Programming (LP)** problem.
